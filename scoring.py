"""
scoring.py â€” Motor de scoring experto EBF
ActÃºa como experto en cerveza artesanal + negocio de festivales
para calificar cada lead y asignar prioridad de contacto.
"""

# â”€â”€â”€ SCORING: CERVECERÃAS (MÃ³dulo A) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def score_cerveceria(c: dict) -> dict:
    """
    EvalÃºa una cervecerÃ­a y devuelve score (0-100) + prioridad + razÃ³n.
    LÃ³gica experta: combina popularidad, calidad, fit geogrÃ¡fico y actividad.
    """
    score = 0
    razones = []

    rating = float(c.get("rating", 0) or 0)
    checkins = int(c.get("checkins", 0) or 0)
    ciudad = str(c.get("ciudad", "")).lower()
    tiene_instagram = bool(c.get("instagram"))
    tiene_web = bool(c.get("sitio_web"))
    ya_estuvo = c.get("participo_EBF_antes", False)
    num_cervezas = int(c.get("num_cervezas", 0) or 0)

    # â”€â”€ Rating Untappd (mÃ¡x 30 pts) â”€â”€
    if rating >= 4.0:
        score += 30
        razones.append("rating excelente (4.0+)")
    elif rating >= 3.7:
        score += 22
        razones.append("rating muy bueno (3.7+)")
    elif rating >= 3.4:
        score += 14
        razones.append("rating bueno (3.4+)")
    elif rating >= 3.0:
        score += 7
    # bajo 3.0 = no suma

    # â”€â”€ Popularidad por check-ins (mÃ¡x 25 pts) â”€â”€
    if checkins >= 50_000:
        score += 25
        razones.append("marca muy popular (+50k check-ins)")
    elif checkins >= 10_000:
        score += 18
        razones.append("popularidad alta (+10k check-ins)")
    elif checkins >= 3_000:
        score += 12
        razones.append("popularidad media (+3k check-ins)")
    elif checkins >= 500:
        score += 6

    # â”€â”€ Fit geogrÃ¡fico (mÃ¡x 20 pts) â”€â”€
    estados_premium = ["baja california", "tijuana", "ensenada", "mexicali"]
    estados_buenos  = ["ciudad de mÃ©xico", "cdmx", "jalisco", "guadalajara",
                       "nuevo leÃ³n", "monterrey", "sonora"]
    if any(e in ciudad for e in estados_premium):
        score += 20
        razones.append("ubicaciÃ³n premium â€” zona Baja California")
    elif any(e in ciudad for e in estados_buenos):
        score += 13
        razones.append("mercado importante para EBF")
    else:
        score += 5  # otras ciudades igual tienen valor

    # â”€â”€ Presencia digital (mÃ¡x 15 pts) â”€â”€
    if tiene_instagram and tiene_web:
        score += 15
        razones.append("presencia digital completa")
    elif tiene_instagram or tiene_web:
        score += 8
        razones.append("presencia digital parcial")

    # â”€â”€ CatÃ¡logo (mÃ¡x 10 pts) â”€â”€
    if num_cervezas >= 10:
        score += 10
        razones.append(f"catÃ¡logo amplio ({num_cervezas} cervezas)")
    elif num_cervezas >= 5:
        score += 6
    elif num_cervezas >= 2:
        score += 3

    # â”€â”€ Ya participÃ³ en EBF: es renovaciÃ³n (bono +5, diferente track) â”€â”€
    if ya_estuvo:
        score += 5
        razones.append("RENOVACIÃ“N â€” ya participÃ³ en EBF")

    # â”€â”€ Prioridad â”€â”€
    if score >= 70:
        prioridad = "ALTA"
    elif score >= 45:
        prioridad = "MEDIA"
    else:
        prioridad = "BAJA"

    return {
        **c,
        "score": score,
        "prioridad": prioridad,
        "tipo_lead": "RENOVACIÃ“N" if ya_estuvo else "NUEVO",
        "razon_score": " | ".join(razones) if razones else "Perfil bÃ¡sico",
    }


# â”€â”€â”€ SCORING: PATROCINADORES (MÃ³dulo D) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# CategorÃ­as de marcas con su fit natural con EBF
# Score base por categorÃ­a + modificadores por tamaÃ±o/actividad
CATEGORIAS_SPONSOR = {
    # Fit DIRECTO con el mundo cervecero
    "insumos_cerveceros":   {"fit": 95, "tier_sugerido": "OFICIAL",   "descripcion": "Malta, lÃºpulo, levaduras, equipo de producciÃ³n"},
    "cerveceria_industrial": {"fit": 80, "tier_sugerido": "NAMING",    "descripcion": "Marcas de cerveza industriales o importadas"},
    "distribuidora_bebidas": {"fit": 85, "tier_sugerido": "OFICIAL",   "descripcion": "Distribuidoras de bebidas alcohÃ³licas"},
    "copa_vasos_merch":     {"fit": 90, "tier_sugerido": "STAND",     "descripcion": "Vasos, copas, merchandising cervecero"},

    # Fit ALTO â€” lifestyle y experiencias
    "turismo_hoteleria":    {"fit": 88, "tier_sugerido": "OFICIAL",   "descripcion": "Hoteles, agencias de viaje, turismo Baja"},
    "restaurantes_food":    {"fit": 82, "tier_sugerido": "STAND",     "descripcion": "Restaurantes, chefs, food trucks"},
    "musica_entretenimiento":{"fit": 78, "tier_sugerido": "OFICIAL",  "descripcion": "Plataformas de mÃºsica, promotoras"},
    "moda_lifestyle":       {"fit": 72, "tier_sugerido": "STAND",     "descripcion": "Ropa, accesorios, marcas de estilo de vida"},

    # Fit MEDIO â€” marcas aspiracionales
    "automotriz":           {"fit": 65, "tier_sugerido": "PREMIER",   "descripcion": "Autos, motos, camionetas â€” activaciÃ³n de marca masiva"},
    "tecnologia":           {"fit": 60, "tier_sugerido": "OFICIAL",   "descripcion": "Apps, gadgets, plataformas digitales"},
    "bancos_fintech":       {"fit": 58, "tier_sugerido": "NAMING",    "descripcion": "Bancos, tarjetas, fintechs â€” naming rights o cashless"},
    "telecomunicaciones":   {"fit": 55, "tier_sugerido": "PREMIER",   "descripcion": "Telcos â€” WiFi del evento, cobertura, activaciÃ³n"},
    "seguros":              {"fit": 50, "tier_sugerido": "OFICIAL",   "descripcion": "Seguros de viaje, salud â€” perfil adulto con ingreso"},
    "energia_bebidas":      {"fit": 70, "tier_sugerido": "STAND",     "descripcion": "Bebidas energÃ©ticas, agua, soft drinks"},

    # Fit OPORTUNISTA â€” pero viable con 7,500 asistentes/dÃ­a
    "banca_premium":        {"fit": 62, "tier_sugerido": "NAMING",    "descripcion": "Amex, Banamex Ã‰lite, HSBC Premier â€” pÃºblico objetivo coincide"},
    "lujo_premium":         {"fit": 55, "tier_sugerido": "PREMIER",   "descripcion": "Relojes, perfumes, marcas premium"},
    "cannabis_cbd":         {"fit": 75, "tier_sugerido": "STAND",     "descripcion": "CBD, wellness â€” mercado adulto, cultura alternativa"},
    "turismo_baja":         {"fit": 92, "tier_sugerido": "OFICIAL",   "descripcion": "SecretarÃ­a de Turismo, Baja California Travel, Visit Ensenada"},
}


def score_patrocinador(p: dict) -> dict:
    """
    EvalÃºa un prospecto de patrocinador y recomienda tier + precio objetivo.
    """
    score = 0
    razones = []

    categoria = p.get("categoria", "").lower().replace(" ", "_")
    tamano = str(p.get("tamano", "")).lower()        # micro / pyme / mediana / grande / corporativo
    tiene_presupuesto_eventos = p.get("patrocina_eventos_previos", False)
    presencia_nacional = p.get("presencia_nacional", False)
    tiene_contacto = bool(p.get("contacto_marketing"))
    nombre = p.get("nombre", "")

    # â”€â”€ Fit de categorÃ­a (mÃ¡x 40 pts) â”€â”€
    cat_data = CATEGORIAS_SPONSOR.get(categoria, {})
    fit = cat_data.get("fit", 40)
    pts_fit = int(fit * 0.4)
    score += pts_fit
    if fit >= 80:
        razones.append(f"categorÃ­a con fit alto para EBF ({fit}%)")
    elif fit >= 60:
        razones.append(f"categorÃ­a viable para EBF ({fit}%)")

    # â”€â”€ TamaÃ±o de empresa (mÃ¡x 30 pts) â”€â”€
    if "corporativo" in tamano or "grande" in tamano:
        score += 30
        razones.append("empresa grande â€” presupuesto de marketing robusto")
    elif "mediana" in tamano:
        score += 20
        razones.append("empresa mediana â€” presupuesto viable")
    elif "pyme" in tamano:
        score += 10
    elif "micro" in tamano:
        score += 4

    # â”€â”€ Historial de patrocinios (mÃ¡x 20 pts) â”€â”€
    if tiene_presupuesto_eventos:
        score += 20
        razones.append("ya patrocina eventos â€” proceso de venta mÃ¡s corto")

    # â”€â”€ Alcance nacional (mÃ¡x 10 pts) â”€â”€
    if presencia_nacional:
        score += 10
        razones.append("presencia nacional â€” ROI de patrocinio amplio")

    # â”€â”€ Tiene contacto directo â”€â”€
    if tiene_contacto:
        score += 5
        razones.append("contacto de marketing identificado")

    # â”€â”€ Tier sugerido segÃºn score + categorÃ­a â”€â”€
    tier_cat = cat_data.get("tier_sugerido", "STAND")
    if score >= 80:
        tier_final = "PREMIER"
        rango_precio = "$300,000 â€“ $500,000+ MXN"
    elif score >= 65:
        tier_final = "NAMING" if tier_cat in ["NAMING", "PREMIER"] else "OFICIAL"
        rango_precio = "$80,000 â€“ $300,000 MXN"
    elif score >= 45:
        tier_final = "OFICIAL"
        rango_precio = "$30,000 â€“ $80,000 MXN"
    else:
        tier_final = "STAND"
        rango_precio = "$15,000 â€“ $30,000 MXN"

    prioridad = "ALTA" if score >= 65 else ("MEDIA" if score >= 40 else "BAJA")

    return {
        **p,
        "score": score,
        "prioridad": prioridad,
        "tier_sugerido": tier_final,
        "rango_precio_objetivo": rango_precio,
        "descripcion_categoria": cat_data.get("descripcion", ""),
        "razon_score": " | ".join(razones) if razones else "Prospecto genÃ©rico",
    }

