"""exportar.py â€” Genera CSV y JSON por mÃ³dulo"""
import csv, json, os
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

CAMPOS_A = ["nombre","ciudad","estado","pais","rating","checkins","num_cervezas",
            "sitio_web","instagram","untappd_url","fuente","participo_EBF_antes",
            "score","prioridad","tipo_lead","razon_score"]

CAMPOS_D = ["nombre","categoria","descripcion_categoria","tamano",
            "patrocina_eventos_previos","presencia_nacional","contacto_marketing",
            "sitio_web","fuente","nota","score","prioridad",
            "tier_sugerido","rango_precio_objetivo","razon_score"]

def guardar(datos: list, nombre_base: str, campos: list):
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    # CSV
    csv_path = os.path.join(OUTPUT_DIR, f"{nombre_base}_{ts}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(datos)
    # JSON
    json_path = os.path.join(OUTPUT_DIR, f"{nombre_base}_{ts}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(datos), "generado": datetime.now().isoformat(),
                   "datos": datos}, f, ensure_ascii=False, indent=2)
    print(f"  ðŸ’¾ {nombre_base}: {csv_path}")
    print(f"  ðŸ’¾ {nombre_base}: {json_path}")
    return csv_path, json_path

