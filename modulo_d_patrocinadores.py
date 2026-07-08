"""
MÃ³dulo D â€” Patrocinadores y Marcas
Busca prospectos de patrocinio en directorios, festivales y web.
Lead type: venta de activaciones / patrocinios $15kâ€“$500k+ MXN
Incluye cualquier marca que se beneficie de llegar a 7,500+ asistentes/dÃ­a.
"""

import requests
from bs4 import BeautifulSoup
import time
from scoring import score_patrocinador, CATEGORIAS_SPONSOR

HEADERS = {"User-Agent": "Mozilla/5.0 (EBF-Scraper/1.0; contacto@ensenadabeerfest.com)"}


# â”€â”€ MARCAS SEED: patrocinadores de festivales similares â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def scrape_patrocinadores_festivales_similares() -> list:
    """
    Extrae marcas que ya patrocinan festivales de cerveza en MX.
    Si una marca paga en otro festival, puede pagar en EBF.
    """
    urls = [
        ("https://cervefest.com.mx", "cervefest"),
        ("https://bajaflavors.com/ensenada-beer-fest-2026-la-gran-fiesta-de-la-cerveza-artesanal-regresa-el-20-y-21-de-marzo/", "ebf2026"),
    ]
    resultados = []
    for url, fuente in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            soup = BeautifulSoup(r.text, "html.parser")

            # Buscar logos/imÃ¡genes de patrocinadores en secciÃ³n "sponsors"
            sponsor_sections = soup.find_all(
                ["section", "div"],
                class_=lambda c: c and any(
                    k in c.lower() for k in ["sponsor", "patrocin", "partner", "marca"]
                ) if c else False
            )
            for sec in sponsor_sections:
                imgs = sec.find_all("img")
                links = sec.find_all("a")
                for img in imgs:
                    alt = img.get("alt", "").strip()
                    if alt and len(alt) > 2:
                        resultados.append({
                            "nombre": alt,
                            "categoria": "insumos_cerveceros",  # default, se puede refinar
                            "tamano": "mediana",
                            "patrocina_eventos_previos": True,
                            "presencia_nacional": True,
                            "contacto_marketing": "",
                            "sitio_web": "",
                            "fuente": f"sponsor_{fuente}",
                            "nota": f"Patrocinador detectado en {fuente}",
                        })
                for a in links:
                    texto = a.get_text(strip=True)
                    if texto and len(texto) > 3:
                        href = a.get("href", "")
                        resultados.append({
                            "nombre": texto,
                            "categoria": "insumos_cerveceros",
                            "tamano": "mediana",
                            "patrocina_eventos_previos": True,
                            "presencia_nacional": True,
                            "contacto_marketing": "",
                            "sitio_web": href,
                            "fuente": f"sponsor_{fuente}",
                            "nota": f"Patrocinador detectado en {fuente}",
                        })
            time.sleep(0.5)
        except Exception as e:
            print(f"  [sponsors_{fuente}] Error: {e}")

    print(f"  âœ… {len(resultados)} marcas detectadas en festivales similares")
    return resultados


# â”€â”€ PROSPECTOS AUTOMOTRICES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def prospectos_automotrices() -> list:
    """
    Marcas de autos que activan en festivales masivos en MÃ©xico.
    7,500 asistentes/dÃ­a = audiencia de compradores adultos con ingreso.
    """
    marcas = [
        {"nombre": "SEAT MÃ©xico",        "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "marketing@seat.com.mx",   "sitio_web": "seat.com.mx"},
        {"nombre": "Volkswagen MÃ©xico",  "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "prensa@vw.com.mx",        "sitio_web": "vw.com.mx"},
        {"nombre": "Toyota MÃ©xico",      "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "marketing@toyota.com.mx", "sitio_web": "toyota.com.mx"},
        {"nombre": "Nissan MÃ©xico",      "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "",                        "sitio_web": "nissan.com.mx"},
        {"nombre": "Jeep MÃ©xico",        "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "",                        "sitio_web": "jeep.com.mx"},
        {"nombre": "Ford MÃ©xico",        "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "",                        "sitio_web": "ford.com.mx"},
        {"nombre": "Honda MÃ©xico",       "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": False, "presencia_nacional": True,  "contacto_marketing": "",                        "sitio_web": "honda.com.mx"},
        {"nombre": "Kia MÃ©xico",         "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "",                        "sitio_web": "kia.com/mx"},
        {"nombre": "RAM Trucks MÃ©xico",  "categoria": "automotriz", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "",                        "sitio_web": "ramtrucks.com.mx"},
    ]
    for m in marcas:
        m["fuente"] = "seed_automotriz"
        m["nota"] = "Activan en festivales masivos â€” propuesta: display de vehÃ­culo + test drive"
    print(f"  âœ… {len(marcas)} prospectos automotrices cargados")
    return marcas


# â”€â”€ PROSPECTOS TURISMO Y HOTELERÃA BAJA â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def prospectos_turismo_baja() -> list:
    """
    80% de asistentes de EBF vienen de fuera de Ensenada.
    Hoteles, aerolÃ­neas y turismo tienen ROI directo.
    """
    marcas = [
        {"nombre": "SecretarÃ­a de Turismo Baja California", "categoria": "turismo_baja",    "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "turismo@bajacalifornia.gob.mx", "sitio_web": "bajacalifornia.travel"},
        {"nombre": "Visit Ensenada",                        "categoria": "turismo_baja",    "tamano": "grande",      "patrocina_eventos_previos": True,  "presencia_nacional": False, "contacto_marketing": "",                               "sitio_web": "visitensenada.com"},
        {"nombre": "Hotel Coral & Marina Ensenada",         "categoria": "turismo_hoteleria","tamano": "mediana",    "patrocina_eventos_previos": False, "presencia_nacional": False, "contacto_marketing": "",                               "sitio_web": "hotelcoral.com"},
        {"nombre": "Las Rosas Hotel Ensenada",              "categoria": "turismo_hoteleria","tamano": "mediana",    "patrocina_eventos_previos": False, "presencia_nacional": False, "contacto_marketing": "",                               "sitio_web": "lasrosas.com"},
        {"nombre": "Aeromexico",                            "categoria": "turismo_baja",    "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "",                               "sitio_web": "aeromexico.com"},
        {"nombre": "Volaris",                               "categoria": "turismo_baja",    "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "contacto_marketing": "marketing@volaris.com",          "sitio_web": "volaris.com"},
        {"nombre": "Airbnb MÃ©xico",                         "categoria": "turismo_hoteleria","tamano": "corporativo", "patrocina_eventos_previos": True, "presencia_nacional": True,  "contacto_marketing": "",                               "sitio_web": "airbnb.mx"},
        {"nombre": "Booking.com MX",                        "categoria": "turismo_hoteleria","tamano": "corporativo", "patrocina_eventos_previos": True, "presencia_nacional": True,  "contacto_marketing": "",                               "sitio_web": "booking.com"},
    ]
    for m in marcas:
        m["fuente"] = "seed_turismo"
        m["nota"] = "80% asistentes EBF son de fuera â€” ROI directo en reservas y vuelos"
    print(f"  âœ… {len(marcas)} prospectos turismo/hotelerÃ­a cargados")
    return marcas


# â”€â”€ PROSPECTOS BEBIDAS Y ESTILO DE VIDA â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def prospectos_bebidas_lifestyle() -> list:
    marcas = [
        # Bebidas no alcohÃ³licas (complemento natural en festival)
        {"nombre": "Topo Chico",         "categoria": "energia_bebidas", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Agua mineral premium â€” fit perfecto con cerveza artesanal"},
        {"nombre": "Agua Ciel",          "categoria": "energia_bebidas", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "HidrataciÃ³n oficial del festival"},
        {"nombre": "Red Bull MÃ©xico",    "categoria": "energia_bebidas", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Activan en festivales masivos â€” stage patrocinado"},
        {"nombre": "Monster Energy MX",  "categoria": "energia_bebidas", "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Perfil joven-adulto â€” coincide con asistente EBF"},
        # Licores / spirits (coexisten con cerveza en festivales)
        {"nombre": "PatrÃ³n Tequila",     "categoria": "distribuidora_bebidas", "tamano": "corporativo", "patrocina_eventos_previos": True, "presencia_nacional": True, "nota": "Premium spirits â€” bar de coctelerÃ­a dentro del festival"},
        {"nombre": "Casa Dragones",      "categoria": "distribuidora_bebidas", "tamano": "grande",      "patrocina_eventos_previos": True, "presencia_nacional": True, "nota": "Tequila artesanal â€” fit cultural con cerveza artesanal"},
        {"nombre": "Mezcal Vago",        "categoria": "distribuidora_bebidas", "tamano": "mediana",     "patrocina_eventos_previos": False,"presencia_nacional": True, "nota": "Mezcal artesanal â€” audiencia compartida con EBF"},
        # CBD / Wellness (mercado emergente en Baja)
        {"nombre": "Serenity CBD MÃ©xico","categoria": "cannabis_cbd",          "tamano": "pyme",        "patrocina_eventos_previos": False,"presencia_nacional": False,"nota": "Stand de productos CBD â€” mercado adulto alternativo"},
    ]
    for m in marcas:
        m["fuente"] = "seed_bebidas_lifestyle"
        m.setdefault("contacto_marketing", "")
        m.setdefault("sitio_web", "")
    print(f"  âœ… {len(marcas)} prospectos bebidas/lifestyle cargados")
    return marcas


# â”€â”€ PROSPECTOS TECH Y FINTECH â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def prospectos_tech_fintech() -> list:
    marcas = [
        {"nombre": "Mercado Pago",   "categoria": "bancos_fintech",   "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Pagos cashless del festival â€” naming de soluciÃ³n de pago"},
        {"nombre": "BBVA MÃ©xico",    "categoria": "banca_premium",    "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Patrocinador financiero oficial â€” ATMs + activaciÃ³n"},
        {"nombre": "Nu MÃ©xico",      "categoria": "bancos_fintech",   "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Nubank â€” perfil joven, digital, coincide con asistente EBF"},
        {"nombre": "Clip MÃ©xico",    "categoria": "bancos_fintech",   "tamano": "grande",      "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Punto de venta para todos los vendors del festival"},
        {"nombre": "Spotify MÃ©xico", "categoria": "tecnologia",       "tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Patrocinio de stage musical + playlist oficial EBF"},
        {"nombre": "Telcel",         "categoria": "telecomunicaciones","tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "WiFi oficial + cobertura 5G del evento"},
        {"nombre": "AT&T MÃ©xico",    "categoria": "telecomunicaciones","tamano": "corporativo", "patrocina_eventos_previos": True,  "presencia_nacional": True,  "nota": "Alternativa a Telcel â€” cobertura y activaciÃ³n digital"},
    ]
    for m in marcas:
        m["fuente"] = "seed_tech_fintech"
        m.setdefault("contacto_marketing", "")
        m.setdefault("sitio_web", "")
    print(f"  âœ… {len(marcas)} prospectos tech/fintech cargados")
    return marcas


# â”€â”€ ORQUESTADOR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def run_modulo_d() -> list:
    print("\nðŸ’¼ MÃ“DULO D â€” Patrocinadores y Marcas")
    print("-" * 45)

    todos = []
    todos += scrape_patrocinadores_festivales_similares()
    todos += prospectos_automotrices()
    todos += prospectos_turismo_baja()
    todos += prospectos_bebidas_lifestyle()
    todos += prospectos_tech_fintech()

    # Deduplicar por nombre
    vistos = set()
    unicos = []
    for p in todos:
        key = p.get("nombre", "").lower().strip()
        if key and len(key) > 2 and key not in vistos:
            vistos.add(key)
            unicos.append(p)

    # Aplicar scoring experto
    print(f"\n  ðŸ§  Aplicando scoring experto a {len(unicos)} prospectos...")
    scored = [score_patrocinador(p) for p in unicos]
    scored.sort(key=lambda x: x["score"], reverse=True)

    altas  = [p for p in scored if p["prioridad"] == "ALTA"]
    medias = [p for p in scored if p["prioridad"] == "MEDIA"]
    bajas  = [p for p in scored if p["prioridad"] == "BAJA"]

    print(f"\n  ðŸ“Š Resultados MÃ³dulo D:")
    print(f"     ðŸ”´ Prioridad ALTA  : {len(altas)}")
    print(f"     ðŸŸ¡ Prioridad MEDIA : {len(medias)}")
    print(f"     âšª Prioridad BAJA  : {len(bajas)}")

    return scored

