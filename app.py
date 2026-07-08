"""
app.py â€” Ensenada Beerfest Lead Dashboard
Web app compartible: https://ebf-leads.streamlit.app
Deploy: streamlit.io (gratis) | Datos: Google Sheets o local
"""

import streamlit as st
import pandas as pd
import json, os, glob
from datetime import datetime

# â”€â”€ CONFIGURACIÃ“N â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.set_page_config(
    page_title="EBF Lead Dashboard",
    page_icon="ðŸº",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center;
    }
    .main-header h1 { color: #f5c518; font-size: 2.2rem; margin: 0; }
    .main-header p  { color: #aab; margin: 0.3rem 0 0; font-size: 1rem; }
    .metric-card {
        background: #1e1e2e; border-radius: 10px; padding: 1rem 1.5rem;
        border-left: 4px solid #f5c518; text-align: center;
    }
    .badge-alta   { background:#e74c3c; color:white; padding:2px 10px; border-radius:12px; font-size:0.8rem; font-weight:bold; }
    .badge-media  { background:#f39c12; color:white; padding:2px 10px; border-radius:12px; font-size:0.8rem; font-weight:bold; }
    .badge-baja   { background:#95a5a6; color:white; padding:2px 10px; border-radius:12px; font-size:0.8rem; font-weight:bold; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# â”€â”€ HEADER â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<div class="main-header">
    <h1>ðŸº Ensenada Beerfest â€” Lead Dashboard</h1>
    <p>Motor de generaciÃ³n de leads y ventas Â· Actualizado automÃ¡ticamente</p>
</div>
""", unsafe_allow_html=True)

# â”€â”€ CARGA DE DATOS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@st.cache_data(ttl=300)  # refresca cada 5 min automÃ¡ticamente
def cargar_datos():
    base = os.path.dirname(os.path.abspath(__file__))

    def leer_json_mas_reciente(patron):
        files = glob.glob(os.path.join(base, patron))
        if not files:
            return pd.DataFrame()
        latest = sorted(files)[-1]
        with open(latest) as f:
            data = json.load(f)
        return pd.DataFrame(data.get("datos", []))

    cervecerias   = leer_json_mas_reciente("leads_cervecerias_*.json")
    patrocinadores = leer_json_mas_reciente("leads_patrocinadores_*.json")
    return cervecerias, patrocinadores

cervecerias_df, patros_df = cargar_datos()

# â”€â”€ SIDEBAR â€” FILTROS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/1a1a2e/f5c518?text=EBF+2026", use_column_width=True)
    st.markdown("---")
    st.markdown("### ðŸŽ¯ Filtros")

    prioridad_filter = st.multiselect(
        "Prioridad", ["ALTA", "MEDIA", "BAJA"],
        default=["ALTA", "MEDIA"]
    )

    st.markdown("---")
    st.markdown("### ðŸ”„ Actualizar datos")
    if st.button("â–¶ Correr Scraper Ahora", type="primary", use_container_width=True):
        with st.spinner("Scrapeando... puede tomar 1-2 minutos"):
            try:
                import subprocess
                result = subprocess.run(
                    ["python", os.path.join(os.path.dirname(__file__), "main.py")],
                    capture_output=True, text=True, timeout=120
                )
                st.success("âœ… Datos actualizados")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### â„¹ï¸ Sobre EBF")
    st.markdown("""
    **Ensenada Beer Fest**  
    Â· 15Âª ediciÃ³n  
    Â· 120+ cervecerÃ­as  
    Â· 7,500 asistentes/dÃ­a  
    Â· 80% visitantes forÃ¡neos  
    """)

# â”€â”€ MÃ‰TRICAS GLOBALES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
col1, col2, col3, col4, col5 = st.columns(5)

total_cerv  = len(cervecerias_df)
total_patro = len(patros_df)
alta_cerv   = len(cervecerias_df[cervecerias_df["prioridad"]=="ALTA"]) if not cervecerias_df.empty else 0
alta_patro  = len(patros_df[patros_df["prioridad"]=="ALTA"]) if not patros_df.empty else 0

col1.metric("ðŸ­ CervecerÃ­as", total_cerv, "vendor spots")
col2.metric("ðŸ’¼ Patrocinadores", total_patro, "prospectos")
col3.metric("ðŸ”´ Alta Prioridad", alta_cerv + alta_patro, "contactar hoy")
col4.metric("ðŸ’° Pipeline Est.", f"${(alta_patro*80_000 + alta_cerv*10_000):,}", "MXN mÃ­nimo")
col5.metric("ðŸ“… Actualizado", datetime.now().strftime("%d/%m %H:%M"), "")

st.markdown("---")

# â”€â”€ TABS PRINCIPALES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
tab_cerv, tab_patro, tab_resumen = st.tabs([
    "ðŸ­ CervecerÃ­as â€” Vendor Spots",
    "ðŸ’¼ Patrocinadores y Marcas",
    "ðŸ“Š Resumen Ejecutivo",
])

# â”€â”€ TAB A: CERVECERÃAS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with tab_cerv:
    st.markdown("### Leads: CervecerÃ­as (Venta de espacio vendor en EBF)")
    st.caption("Precio objetivo por vendor: $5,000 â€“ $20,000 MXN")

    if cervecerias_df.empty:
        st.info("âš ï¸ Sin datos de cervecerÃ­as todavÃ­a. Agrega tus credenciales de Untappd en `config.py` y corre el scraper.")
        st.code("""
# 1. RegÃ­strate gratis en: https://untappd.com/api/register
# 2. Abre config.py y pega:
UNTAPPD_CLIENT_ID     = "tu_id_aqui"
UNTAPPD_CLIENT_SECRET = "tu_secret_aqui"
# 3. Click "Correr Scraper Ahora" en el sidebar
        """)
    else:
        df = cervecerias_df.copy()
        if prioridad_filter:
            df = df[df["prioridad"].isin(prioridad_filter)]

        # Filtros adicionales
        c1, c2 = st.columns(2)
        with c1:
            estados_disp = ["Todos"] + sorted(df["estado"].dropna().unique().tolist())
            estado_sel = st.selectbox("Estado", estados_disp)
            if estado_sel != "Todos":
                df = df[df["estado"] == estado_sel]
        with c2:
            tipo_sel = st.selectbox("Tipo de lead", ["Todos", "NUEVO", "RENOVACIÃ“N"])
            if tipo_sel != "Todos":
                df = df[df["tipo_lead"] == tipo_sel]

        # Tabla con colores
        def color_prioridad(val):
            colores = {"ALTA": "background-color:#2d0000;color:#ff6b6b",
                       "MEDIA": "background-color:#2d1a00;color:#ffa94d",
                       "BAJA": "background-color:#1a1a1a;color:#888"}
            return colores.get(val, "")

        cols_mostrar = [c for c in ["nombre","ciudad","estado","rating","checkins","prioridad","score","tipo_lead","razon_score","sitio_web"] if c in df.columns]
        st.dataframe(
            df[cols_mostrar].style.applymap(color_prioridad, subset=["prioridad"]),
            use_container_width=True, height=450
        )
        st.caption(f"{len(df)} cervecerÃ­as Â· ordenadas por score")

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button("â¬‡ï¸ Descargar CSV", df.to_csv(index=False).encode(),
                               "leads_cervecerias.csv", "text/csv", use_container_width=True)

# â”€â”€ TAB D: PATROCINADORES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with tab_patro:
    st.markdown("### Leads: Patrocinadores y Marcas")
    st.caption("Rangos: Stand $15k â€“ $80k Â· Oficial $80k â€“ $300k Â· Naming $300k â€“ $500k Â· Premier $500k+ MXN")

    if patros_df.empty:
        st.info("Sin datos de patrocinadores.")
    else:
        df = patros_df.copy()
        if prioridad_filter:
            df = df[df["prioridad"].isin(prioridad_filter)]

        c1, c2, c3 = st.columns(3)
        with c1:
            cats = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
            cat_sel = st.selectbox("CategorÃ­a", cats)
            if cat_sel != "Todas":
                df = df[df["categoria"] == cat_sel]
        with c2:
            tiers = ["Todos"] + sorted(df["tier_sugerido"].dropna().unique().tolist())
            tier_sel = st.selectbox("Tier", tiers)
            if tier_sel != "Todos":
                df = df[df["tier_sugerido"] == tier_sel]
        with c3:
            score_min = st.slider("Score mÃ­nimo", 0, 100, 40)
            df = df[df["score"] >= score_min]

        def color_tier(val):
            colores = {
                "PREMIER":  "background-color:#1a0a2e;color:#c084fc",
                "NAMING":   "background-color:#0a1a2e;color:#60a5fa",
                "OFICIAL":  "background-color:#0a2e1a;color:#34d399",
                "STAND":    "background-color:#2e2a0a;color:#fbbf24",
            }
            return colores.get(val, "")

        cols_mostrar = [c for c in ["nombre","categoria","tier_sugerido","rango_precio_objetivo","score","prioridad","nota","contacto_marketing"] if c in df.columns]
        st.dataframe(
            df[cols_mostrar].style
                .applymap(color_tier, subset=["tier_sugerido"])
                .applymap(lambda v: "color:#ff6b6b;font-weight:bold" if v=="ALTA" else "", subset=["prioridad"]),
            use_container_width=True, height=450
        )
        st.caption(f"{len(df)} prospectos")

        # Top 5 destacados
        st.markdown("#### ðŸ† Top 5 â€” Atacar primero")
        top5 = df.nlargest(5, "score")[["nombre","tier_sugerido","rango_precio_objetivo","razon_score"]]
        for _, row in top5.iterrows():
            with st.expander(f"**{row['nombre']}** Â· {row['tier_sugerido']} Â· {row['rango_precio_objetivo']}"):
                st.write(row["razon_score"])

        st.download_button("â¬‡ï¸ Descargar CSV", df.to_csv(index=False).encode(),
                           "leads_patrocinadores.csv", "text/csv")

# â”€â”€ TAB RESUMEN â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with tab_resumen:
    st.markdown("### ðŸ“Š Resumen Ejecutivo â€” EBF Sales Pipeline")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### MÃ³dulo D â€” Patrocinadores por Tier")
        if not patros_df.empty:
            tier_counts = patros_df["tier_sugerido"].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Cantidad"]
            st.dataframe(tier_counts, use_container_width=True, hide_index=True)

            # Estimado de ingresos
            rangos = {"STAND": 47_500, "OFICIAL": 190_000, "NAMING": 400_000, "PREMIER": 500_000}
            patros_df["ingreso_estimado"] = patros_df["tier_sugerido"].map(rangos).fillna(0)
            alta = patros_df[patros_df["prioridad"]=="ALTA"]
            total_est = alta["ingreso_estimado"].sum()
            st.metric("ðŸ’° Potencial leads ALTA (patrocinadores)", f"${total_est:,.0f} MXN",
                      f"{len(alta)} prospectos de alta prioridad")

    with col_b:
        st.markdown("#### MÃ³dulo A â€” CervecerÃ­as por Estado")
        if not cervecerias_df.empty:
            estado_counts = cervecerias_df.groupby(["estado","prioridad"]).size().reset_index(name="n")
            st.dataframe(estado_counts, use_container_width=True, hide_index=True)
        else:
            st.info("Pendiente: conectar Untappd API en config.py")

    st.markdown("---")
    st.markdown("""
    #### ðŸ—ºï¸ Roadmap del Scraper
    | MÃ³dulo | Estado | Objetivo de venta |
    |--------|--------|-------------------|
    | **A â€” CervecerÃ­as** | ðŸ”§ Pendiente Untappd API | Vendor spots $5kâ€“$20k |
    | **B â€” Entusiastas** | â³ En construcciÃ³n | Boletos $300â€“$1,500 |
    | **C â€” Talleres/Escuelas** | â³ En construcciÃ³n | Espacio taller + co-promo |
    | **D â€” Patrocinadores** | âœ… Activo (32 leads) | Patrocinios $15kâ€“$500k+ |
    """)

