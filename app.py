"""
app.py — Ensenada Beerfest Lead Dashboard
"""

import streamlit as st
import pandas as pd
import json, os, glob
from datetime import datetime

st.set_page_config(
    page_title="EBF Lead Dashboard",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center;
    }
    .main-header h1 { color: #f5c518; font-size: 2.2rem; margin: 0; font-family: sans-serif; }
    .main-header p  { color: #aabbcc; margin: 0.3rem 0 0; font-size: 1rem; font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Ensenada Beerfest — Lead Dashboard</h1>
    <p>Motor de generacion de leads y ventas · Actualizado automaticamente</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def cargar_datos():
    base = os.path.dirname(os.path.abspath(__file__))
    def leer_json(patron):
        files = glob.glob(os.path.join(base, patron))
        if not files:
            return pd.DataFrame()
        with open(sorted(files)[-1]) as f:
            data = json.load(f)
        return pd.DataFrame(data.get("datos", []))
    return leer_json("leads_cervecerias_*.json"), leer_json("leads_patrocinadores_*.json")

cervecerias_df, patros_df = cargar_datos()

with st.sidebar:
    st.markdown("### Filtros")
    prioridad_filter = st.multiselect(
        "Prioridad", ["ALTA", "MEDIA", "BAJA"], default=["ALTA", "MEDIA"]
    )
    st.markdown("---")
    st.markdown("### Actualizar datos")
    if st.button("Correr Scraper Ahora", type="primary", use_container_width=True):
        with st.spinner("Scrapeando..."):
            try:
                import subprocess
                subprocess.run(
                    ["python", os.path.join(os.path.dirname(__file__), "main.py")],
                    capture_output=True, text=True, timeout=120
                )
                st.success("Datos actualizados")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    st.markdown("---")
    st.markdown("**Ensenada Beer Fest**")
    st.markdown("- 15a edicion\n- 120+ cervecerias\n- 7,500 asistentes/dia\n- 80% visitantes foraneos")

col1, col2, col3, col4, col5 = st.columns(5)
total_cerv  = len(cervecerias_df)
total_patro = len(patros_df)
alta_cerv   = len(cervecerias_df[cervecerias_df["prioridad"]=="ALTA"]) if not cervecerias_df.empty else 0
alta_patro  = len(patros_df[patros_df["prioridad"]=="ALTA"]) if not patros_df.empty else 0

col1.metric("Cervecerias", total_cerv, "vendor spots")
col2.metric("Patrocinadores", total_patro, "prospectos")
col3.metric("Alta Prioridad", alta_cerv + alta_patro, "contactar hoy")
col4.metric("Pipeline Est.", f"${(alta_patro*80_000 + alta_cerv*10_000):,}", "MXN minimo")
col5.metric("Actualizado", datetime.now().strftime("%d/%m %H:%M"), "")

st.markdown("---")

tab_cerv, tab_patro, tab_resumen = st.tabs([
    "Cervecerias — Vendor Spots",
    "Patrocinadores y Marcas",
    "Resumen Ejecutivo",
])

with tab_cerv:
    st.markdown("### Leads: Cervecerias")
    st.caption("Precio objetivo por vendor: $5,000 - $20,000 MXN")
    if cervecerias_df.empty:
        st.info("Sin datos de cervecerias. Agrega tus credenciales de Untappd en config.py y corre el scraper.")
        st.code("""# 1. Registrate en: https://untappd.com/api/register
# 2. Abre config.py y pega:
UNTAPPD_CLIENT_ID     = "tu_id"
UNTAPPD_CLIENT_SECRET = "tu_secret"
# 3. Click 'Correr Scraper Ahora'""")
    else:
        df = cervecerias_df.copy()
        if prioridad_filter:
            df = df[df["prioridad"].isin(prioridad_filter)]
        cols = [c for c in ["nombre","ciudad","estado","rating","checkins","prioridad","score","tipo_lead","razon_score","sitio_web"] if c in df.columns]
        st.dataframe(df[cols], use_container_width=True, height=450)
        st.download_button("Descargar CSV", df.to_csv(index=False).encode(), "leads_cervecerias.csv", "text/csv")

with tab_patro:
    st.markdown("### Leads: Patrocinadores y Marcas")
    st.caption("Rangos: Stand $15k-$80k | Oficial $80k-$300k | Naming $300k-$500k | Premier $500k+ MXN")
    if patros_df.empty:
        st.info("Sin datos de patrocinadores.")
    else:
        df = patros_df.copy()
        if prioridad_filter:
            df = df[df["prioridad"].isin(prioridad_filter)]

        c1, c2, c3 = st.columns(3)
        with c1:
            cats = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
            cat_sel = st.selectbox("Categoria", cats)
            if cat_sel != "Todas":
                df = df[df["categoria"] == cat_sel]
        with c2:
            tiers = ["Todos"] + sorted(df["tier_sugerido"].dropna().unique().tolist())
            tier_sel = st.selectbox("Tier", tiers)
            if tier_sel != "Todos":
                df = df[df["tier_sugerido"] == tier_sel]
        with c3:
            score_min = st.slider("Score minimo", 0, 100, 40)
            df = df[df["score"] >= score_min]

        cols = [c for c in ["nombre","categoria","tier_sugerido","rango_precio_objetivo","score","prioridad","nota","contacto_marketing"] if c in df.columns]
        st.dataframe(df[cols], use_container_width=True, height=400)
        st.caption(f"{len(df)} prospectos")

        st.markdown("#### Top 5 — Atacar primero")
        top5 = df.nlargest(5, "score")[["nombre","tier_sugerido","rango_precio_objetivo","razon_score"]]
        for _, row in top5.iterrows():
            with st.expander(f"{row['nombre']}  |  {row['tier_sugerido']}  |  {row['rango_precio_objetivo']}"):
                st.write(row["razon_score"])

        st.download_button("Descargar CSV", df.to_csv(index=False).encode(), "leads_patrocinadores.csv", "text/csv")

with tab_resumen:
    st.markdown("### Resumen Ejecutivo — EBF Sales Pipeline")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Patrocinadores por Tier")
        if not patros_df.empty:
            tier_counts = patros_df["tier_sugerido"].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Cantidad"]
            st.dataframe(tier_counts, use_container_width=True, hide_index=True)
            rangos = {"STAND": 47_500, "OFICIAL": 190_000, "NAMING": 400_000, "PREMIER": 500_000}
            patros_df["ingreso_estimado"] = patros_df["tier_sugerido"].map(rangos).fillna(0)
            alta = patros_df[patros_df["prioridad"]=="ALTA"]
            st.metric("Potencial leads ALTA", f"${alta['ingreso_estimado'].sum():,.0f} MXN", f"{len(alta)} prospectos")
    with col_b:
        st.markdown("#### Cervecerias por Estado")
        if not cervecerias_df.empty:
            st.dataframe(cervecerias_df.groupby(["estado","prioridad"]).size().reset_index(name="n"), use_container_width=True, hide_index=True)
        else:
            st.info("Pendiente: conectar Untappd API en config.py")

    st.markdown("---")
    st.markdown("#### Roadmap del Scraper")
    st.table(pd.DataFrame({
        "Modulo": ["A - Cervecerias", "B - Entusiastas", "C - Talleres/Escuelas", "D - Patrocinadores"],
        "Estado": ["Pendiente Untappd API", "En construccion", "En construccion", "Activo (32 leads)"],
        "Objetivo de venta": ["Vendor spots $5k-$20k", "Boletos $300-$1,500", "Espacio taller + co-promo", "Patrocinios $15k-$500k+"],
    }))
