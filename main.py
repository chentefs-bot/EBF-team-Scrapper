#!/usr/bin/env python3
"""
main.py â€” Ensenada Beerfest Lead Generation Scraper
Corre todos los mÃ³dulos activos y exporta CSV + JSON para Google Sheets.

USO:
    python main.py                  # corre todos los mÃ³dulos
    python main.py --modulo a       # solo MÃ³dulo A (cervecerÃ­as)
    python main.py --modulo d       # solo MÃ³dulo D (patrocinadores)
"""

import sys
from datetime import datetime
from modulo_a_cervecerias import run_modulo_a
from modulo_d_patrocinadores import run_modulo_d
from exportar import guardar, CAMPOS_A, CAMPOS_D

def main():
    modulo_arg = None
    if "--modulo" in sys.argv:
        idx = sys.argv.index("--modulo")
        if idx + 1 < len(sys.argv):
            modulo_arg = sys.argv[idx + 1].lower()

    print("=" * 50)
    print("ðŸº  EBF LEAD GENERATION SCRAPER")
    print(f"    {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    if modulo_arg in (None, "a"):
        leads_cervecerias = run_modulo_a()
        guardar(leads_cervecerias, "leads_cervecerias", CAMPOS_A)

    if modulo_arg in (None, "d"):
        leads_patrocinadores = run_modulo_d()
        guardar(leads_patrocinadores, "leads_patrocinadores", CAMPOS_D)

    print("\nâœ… SCRAPER TERMINADO")
    print("   â†’ Importa los CSV a Google Sheets (EBF CRM)")
    print("   â†’ Filtra por columna 'prioridad' = ALTA para atacar primero")

if __name__ == "__main__":
    main()

