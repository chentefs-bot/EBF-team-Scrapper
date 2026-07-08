# config.py â€” Ensenada Beerfest Scraper
# Llena tus credenciales aquÃ­ antes de correr

# â”€â”€ Untappd API (gratis: https://untappd.com/api/register) â”€â”€
UNTAPPD_CLIENT_ID     = "TU_CLIENT_ID_AQUI"
UNTAPPD_CLIENT_SECRET = "TU_CLIENT_SECRET_AQUI"

# â”€â”€ Estados prioritarios para buscar cervecerÃ­as â”€â”€
ESTADOS_PRIORIDAD = [
    "Baja California",
    "Ciudad de MÃ©xico",
    "Jalisco",
    "Nuevo LeÃ³n",
    "Sonora",
]

# â”€â”€ CervecerÃ­as que ya participaron en EBF (marcar como "renovaciÃ³n") â”€â”€
CERVECERIAS_EBF_ANTERIORES = [
    # "CervecerÃ­a Insurgente",
    # "Agua Mala",
    # "Wendlandt",
]

# â”€â”€ Rangos de patrocinio EBF (MXN) â”€â”€
TIER_STAND       = (15_000,  80_000)   # Stand / activaciÃ³n bÃ¡sica
TIER_OFICIAL     = (80_001,  300_000)  # Patrocinador oficial
TIER_NAMING      = (300_001, 500_000)  # Naming rights / patrocinador principal
TIER_PREMIER     = (500_001, 9_999_999) # Premier â€” negociable caso por caso

# â”€â”€ Output â”€â”€
OUTPUT_DIR = "."

