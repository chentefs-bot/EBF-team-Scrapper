"""
MÃ³dulo A â€” CervecerÃ­as
Scrapes directorios de cervecerÃ­as MX + Untappd API
Lead type: venta de vendor spots en EBF
"""

import requests
from bs4 import BeautifulSoup
import time
from config import (UNTAPPD_CLIENT_ID, UNTAPPD_CLIENT_SECRET,
                    ESTADOS_PRIORIDAD, CERVECERIAS_EBF_ANTERIORES)
from scoring import score_cerveceria

HEADERS = {"User-Agent": "Mozilla/5.0 (EBF-Scraper/1.0; contacto@ensenadabeerfest.com)"}


# â”€â”€ UNTAPPD API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def buscar_cervecerias_untappd(query: str, limit: int = 25) -> list:
    """
    Busca cervecerÃ­as en Untappd por nombre o ciudad.
    Requiere client_id y client_secret de Untappd Developer.
    """
    if UNTAPPD_CLIENT_ID == "TU_CLIENT_ID_AQUI":
        print("  [Untappd] âš ï¸  Agrega tus credenciales en config.py")
        return []

    url = "https://api.untappd.com/v4/search/brewery"
    params = {
        "client_id": UNTAPPD_CLIENT_ID,
        "client_secret": UNTAPPD_CLIENT_SECRET,
        "q": query,
        "limit": limit,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        items = data.get("response", {}).get("brewery", {}).get("items", [])
        resultados = []
        for item in items:
            b = item.get("brewery", {})
            loc = b.get("location", {})
            stats = b.get("stats", {})
            contact = b.get("contact", {})
            resultados.append({
                "nombre": b.get("brewery_name", ""),
                "ciudad": loc.get("brewery_city", ""),
                "estado": loc.get("brewery_state", ""),
                "pais": loc.get("country_name", ""),
                "rating": round(b.get("rating", {}).get("rating_score", 0), 2),
                "checkins": stats.get("total_count", 0),
                "num_cervezas": b.get("beer_count", 0),
                "sitio_web": contact.get("url", ""),
                "instagram": contact.get("instagram", ""),
                "untappd_url": f"https://untappd.com/brewery/{b.get('brewery_id','')}",
                "fuente": "untappd_api",
                "participo_EBF_antes": b.get("brewery_name", "") in CERVECERIAS_EBF_ANTERIORES,
            })
        return resultados
    except Exception as e:
        print(f"  [Untappd] Error: {e}")
        return []


def obtener_cervecerias_untappd_mexico() -> list:
    """Busca cervecerÃ­as en los estados prioritarios vÃ­a Untappd API."""
    print("  ðŸ“¡ Consultando Untappd API...")
    todas = []
    queries = ["cervecerÃ­a MÃ©xico", "craft beer Baja California",
               "cervecerÃ­a Jalisco", "cerveza artesanal CDMX",
               "microcervecerÃ­a Monterrey", "brewery Ensenada",
               "cervecerÃ­a Tijuana", "craft beer Sonora"]
    for q in queries:
        results = buscar_cervecerias_untappd(q)
        todas.extend(results)
        time.sleep(0.5)  # respetar rate limit de Untappd

    # Deduplicar por nombre
    vistos = set()
    unicas = []
    for c in todas:
        key = c["nombre"].lower().strip()
        if key and key not in vistos:
            vistos.add(key)
            unicas.append(c)
    print(f"  âœ… {len(unicas)} cervecerÃ­as Ãºnicas de Untappd")
    return unicas


# â”€â”€ DIRECTORIO WEB: cerveceriasmexico.com â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def scrape_cerveceriasmexico() -> list:
    """Scrape del directorio cerveceriasmexico.com"""
    base_url = "https://www.cerveceriasmexico.com"
    resultados = []
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Buscar listados de cervecerÃ­as
        cards = soup.find_all(["article", "div", "li"],
                               class_=lambda c: c and any(
                                   k in c.lower() for k in ["cerveceria", "brewery", "listing", "card"]
                               ))
        for card in cards[:50]:
            nombre_el = card.find(["h2", "h3", "h4", "strong"])
            ciudad_el = card.find(["span", "p"],
                                   class_=lambda c: c and "city" in c.lower() if c else False)
            link_el = card.find("a")
            if not nombre_el:
                continue
            nombre = nombre_el.get_text(strip=True)
            if len(nombre) < 3:
                continue
            resultados.append({
                "nombre": nombre,
                "ciudad": ciudad_el.get_text(strip=True) if ciudad_el else "",
                "estado": "",
                "pais": "MÃ©xico",
                "rating": 0,
                "checkins": 0,
                "num_cervezas": 0,
                "sitio_web": link_el["href"] if link_el and link_el.get("href") else "",
                "instagram": "",
                "untappd_url": "",
                "fuente": "cerveceriasmexico.com",
                "participo_EBF_antes": nombre in CERVECERIAS_EBF_ANTERIORES,
            })
        print(f"  âœ… {len(resultados)} cervecerÃ­as de cerveceriasmexico.com")
    except Exception as e:
        print(f"  [cerveceriasmexico] Error: {e}")
    return resultados


# â”€â”€ SCRAPE: CervecerÃ­as en Google Maps (via bÃºsqueda web) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def scrape_cervecerias_google_maps_fallback() -> list:
    """
    BÃºsqueda de respaldo: scrapea resultados de bÃºsqueda de Google
    cuando no hay API disponible. Solo extrae nombres y URLs bÃ¡sicos.
    """
    queries = [
        "microcervecerÃ­a artesanal Baja California",
        "cervecerÃ­a artesanal Ensenada",
        "craft brewery Tijuana",
    ]
    resultados = []
    for q in queries:
        try:
            url = f"https://www.google.com/search?q={q.replace(' ', '+')}&num=20"
            r = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            # Extraer snippets de resultados orgÃ¡nicos
            for div in soup.find_all("div", class_="BNeawe"):
                texto = div.get_text(strip=True)
                if len(texto) > 10 and "cervec" in texto.lower():
                    resultados.append({
                        "nombre": texto[:80],
                        "ciudad": "Baja California",
                        "estado": "Baja California",
                        "pais": "MÃ©xico",
                        "rating": 0, "checkins": 0, "num_cervezas": 0,
                        "sitio_web": "", "instagram": "", "untappd_url": "",
                        "fuente": "google_search",
                        "participo_EBF_antes": False,
                    })
            time.sleep(1)
        except Exception as e:
            print(f"  [google_fallback] Error en '{q}': {e}")
    print(f"  âœ… {len(resultados)} resultados de bÃºsqueda web (fallback)")
    return resultados


# â”€â”€ ORQUESTADOR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def run_modulo_a() -> list:
    print("\nðŸ­ MÃ“DULO A â€” CervecerÃ­as (Vendor Spots)")
    print("-" * 45)

    todas = []
    todas += obtener_cervecerias_untappd_mexico()
    todas += scrape_cerveceriasmexico()

    if not todas:
        print("  âš ï¸  Sin resultados de APIs â€” usando bÃºsqueda web de respaldo")
        todas += scrape_cervecerias_google_maps_fallback()

    # Deduplicar globalmente
    vistos = set()
    unicas = []
    for c in todas:
        key = c.get("nombre", "").lower().strip()
        if key and len(key) > 2 and key not in vistos:
            vistos.add(key)
            unicas.append(c)

    # Aplicar scoring experto
    print(f"\n  ðŸ§  Aplicando scoring experto a {len(unicas)} cervecerÃ­as...")
    scored = [score_cerveceria(c) for c in unicas]

    # Ordenar por score descendente
    scored.sort(key=lambda x: x["score"], reverse=True)

    altas  = [c for c in scored if c["prioridad"] == "ALTA"]
    medias = [c for c in scored if c["prioridad"] == "MEDIA"]
    bajas  = [c for c in scored if c["prioridad"] == "BAJA"]

    print(f"\n  ðŸ“Š Resultados MÃ³dulo A:")
    print(f"     ðŸ”´ Prioridad ALTA  : {len(altas)}")
    print(f"     ðŸŸ¡ Prioridad MEDIA : {len(medias)}")
    print(f"     âšª Prioridad BAJA  : {len(bajas)}")

    return scored

