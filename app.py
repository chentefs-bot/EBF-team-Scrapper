"""
app.py — Ensenada Beerfest Lead Dashboard
Datos de Módulo D embebidos directamente — funciona sin archivos locales.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="EBF Lead Dashboard", page_icon="🍺", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center;
}
.main-header h1 { color: #f5c518; font-size: 2.2rem; margin: 0; font-family: sans-serif; }
.main-header p  { color: #aabbcc; margin: 0.3rem 0 0; font-size: 1rem; font-family: sans-serif; }
</style>
<div class="main-header">
    <h1>Ensenada Beerfest — Lead Dashboard</h1>
    <p>Motor de generacion de leads y ventas · Modulo D activo · Actualizado automaticamente</p>
</div>
""", unsafe_allow_html=True)

# ── DATOS EMBEBIDOS: MÓDULO D — PATROCINADORES ────────────────────────────────
PATROCINADORES = [
    # TURISMO / BAJA — fit directo con EBF (80% visitantes foraneos)
    {"nombre":"Secretaria de Turismo Baja California","categoria":"turismo_baja","tamano":"corporativo","score":101,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Fit directo — 80% asistentes son foraneos, turismo BC tiene ROI inmediato","contacto_marketing":"turismo@bajacalifornia.gob.mx"},
    {"nombre":"Visit Ensenada","categoria":"turismo_baja","tamano":"grande","score":96,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Co-organizador natural del evento — presencia de marca en toda la comunicacion","contacto_marketing":""},
    {"nombre":"Volaris","categoria":"turismo_baja","tamano":"corporativo","score":101,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"80% asistentes vienen de fuera — aerolinea con rutas a Tijuana/Ensenada","contacto_marketing":"marketing@volaris.com"},
    {"nombre":"Aeromexico","categoria":"turismo_baja","tamano":"corporativo","score":96,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Ruta CDMX-Tijuana — audiencia premium que asiste a EBF","contacto_marketing":""},
    {"nombre":"Airbnb Mexico","categoria":"turismo_hoteleria","tamano":"corporativo","score":95,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Plataforma de hospedaje — patrocina festivales masivos, audiencia coincide 100%","contacto_marketing":""},
    {"nombre":"Booking.com MX","categoria":"turismo_hoteleria","tamano":"corporativo","score":95,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Hospedaje oficial del festival — banner en boletos y comunicacion","contacto_marketing":""},
    {"nombre":"Hotel Coral & Marina Ensenada","categoria":"turismo_hoteleria","tamano":"mediana","score":70,"prioridad":"MEDIA","tier_sugerido":"OFICIAL","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Hotel premium local — paquetes festival+hospedaje","contacto_marketing":""},
    # BEBIDAS — fit natural
    {"nombre":"Patron Tequila","categoria":"distribuidora_bebidas","tamano":"corporativo","score":94,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Premium spirits — bar de cocteleria dentro del festival, audiencia adulta con ingreso","contacto_marketing":""},
    {"nombre":"Casa Dragones","categoria":"distribuidora_bebidas","tamano":"grande","score":94,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Tequila artesanal — fit cultural identico con cerveza artesanal","contacto_marketing":""},
    {"nombre":"Mezcal Vago","categoria":"distribuidora_bebidas","tamano":"mediana","score":78,"prioridad":"ALTA","tier_sugerido":"OFICIAL","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Mezcal artesanal — audiencia compartida con EBF, cultura alternativa","contacto_marketing":""},
    {"nombre":"Topo Chico","categoria":"energia_bebidas","tamano":"corporativo","score":85,"prioridad":"ALTA","tier_sugerido":"OFICIAL","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Agua mineral premium — complemento perfecto de cerveza artesanal, hidratacion oficial","contacto_marketing":""},
    {"nombre":"Red Bull Mexico","categoria":"energia_bebidas","tamano":"corporativo","score":82,"prioridad":"ALTA","tier_sugerido":"OFICIAL","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Stage patrocinado Red Bull — activan en festivales masivos","contacto_marketing":""},
    # AUTOMOTRIZ — activacion de marca masiva
    {"nombre":"SEAT Mexico","categoria":"automotriz","tamano":"corporativo","score":91,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Display de vehiculo + test drive — 7,500 personas/dia son compradores potenciales","contacto_marketing":"marketing@seat.com.mx"},
    {"nombre":"Volkswagen Mexico","categoria":"automotriz","tamano":"corporativo","score":91,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Activacion de marca — audiencia adulta con poder adquisitivo medio-alto","contacto_marketing":"prensa@vw.com.mx"},
    {"nombre":"Toyota Mexico","categoria":"automotriz","tamano":"corporativo","score":91,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Festival de fin de semana — target de compradores de SUVs y pick-ups","contacto_marketing":""},
    {"nombre":"Jeep Mexico","categoria":"automotriz","tamano":"corporativo","score":91,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Perfil aventurero — festival al aire libre en Ensenada es fit natural para Jeep","contacto_marketing":""},
    {"nombre":"RAM Trucks Mexico","categoria":"automotriz","tamano":"corporativo","score":91,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"Baja California = territorio RAM — activacion premium en festival icono de la region","contacto_marketing":""},
    # TECH / FINTECH
    {"nombre":"Mercado Pago","categoria":"bancos_fintech","tamano":"corporativo","score":88,"prioridad":"ALTA","tier_sugerido":"NAMING","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Pagos cashless del festival — naming 'EBF powered by Mercado Pago'","contacto_marketing":""},
    {"nombre":"Nu Mexico (Nubank)","categoria":"bancos_fintech","tamano":"corporativo","score":85,"prioridad":"ALTA","tier_sugerido":"NAMING","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Perfil joven-digital — coincide exactamente con asistente tipico de EBF","contacto_marketing":""},
    {"nombre":"Clip Mexico","categoria":"bancos_fintech","tamano":"grande","score":80,"prioridad":"ALTA","tier_sugerido":"OFICIAL","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Punto de venta para todos los vendors — presencia en cada stand del festival","contacto_marketing":""},
    {"nombre":"Spotify Mexico","categoria":"tecnologia","tamano":"corporativo","score":82,"prioridad":"ALTA","tier_sugerido":"OFICIAL","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Patrocinio de stage musical + playlist oficial EBF 2026","contacto_marketing":""},
    {"nombre":"Telcel","categoria":"telecomunicaciones","tamano":"corporativo","score":78,"prioridad":"ALTA","tier_sugerido":"PREMIER","rango_precio_objetivo":"$300,000 – $500,000+ MXN","nota":"WiFi oficial + cobertura 5G del evento — 15,000 personas en 2 dias","contacto_marketing":""},
    {"nombre":"BBVA Mexico","categoria":"banca_premium","tamano":"corporativo","score":75,"prioridad":"ALTA","tier_sugerido":"NAMING","rango_precio_objetivo":"$80,000 – $300,000 MXN","nota":"Patrocinador financiero oficial — ATMs en el festival + activacion de tarjeta","contacto_marketing":""},
]

df_patros = pd.DataFrame(PATROCINADORES)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filtros")
    prioridad_filter = st.multiselect("Prioridad", ["ALTA", "MEDIA", "BAJA"], default=["ALTA", "MEDIA"])
    tier_filter = st.multiselect("Tier", ["PREMIER", "NAMING", "OFICIAL", "STAND"], default=["PREMIER", "NAMING", "OFICIAL"])
    st.markdown("---")
    st.markdown("**Ensenada Beer Fest**")
    st.markdown("- 15a edicion (2026)\n- 120+ cervecerias\n- 7,500 asistentes/dia\n- 80% visitantes foraneos\n- Copa Cervecera del Pacifico")
    st.markdown("---")
    st.caption(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ── METRICAS ──────────────────────────────────────────────────────────────────
df_alta = df_patros[df_patros["prioridad"]=="ALTA"]
pipeline_min = len(df_alta) * 80_000

col1, col2, col3, col4 = st.columns(4)
col1.metric("Prospectos totales", len(df_patros), "patrocinadores identificados")
col2.metric("Alta prioridad", len(df_alta), "contactar esta semana")
col3.metric("Pipeline estimado minimo", f"${pipeline_min:,}", "MXN — leads ALTA")
col4.metric("Tier Premier identificados", len(df_patros[df_patros["tier_sugerido"]=="PREMIER"]), "marcas $300k+")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Patrocinadores y Marcas", "Cervecerias — Vendor Spots", "Resumen Ejecutivo"])

with tab1:
    st.markdown("### Prospectos de Patrocinio — EBF 2026")
    st.caption("Rangos: Stand $15k-$80k | Oficial $80k-$300k | Naming $300k-$500k | Premier $500k+ MXN")

    df = df_patros.copy()
    if prioridad_filter:
        df = df[df["prioridad"].isin(prioridad_filter)]
    if tier_filter:
        df = df[df["tier_sugerido"].isin(tier_filter)]

    c1, c2 = st.columns(2)
    with c1:
        cats = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
        cat_sel = st.selectbox("Categoria", cats)
        if cat_sel != "Todas":
            df = df[df["categoria"] == cat_sel]
    with c2:
        score_min = st.slider("Score minimo", 0, 101, 70)
        df = df[df["score"] >= score_min]

    cols_tabla = ["nombre","categoria","tier_sugerido","rango_precio_objetivo","score","prioridad","nota","contacto_marketing"]
    st.dataframe(df[cols_tabla], use_container_width=True, height=420)
    st.caption(f"{len(df)} prospectos mostrados")

    st.download_button("Descargar CSV de patrocinadores", df.to_csv(index=False).encode("utf-8"), "leads_patrocinadores_ebf.csv", "text/csv", use_container_width=True)

    st.markdown("---")
    st.markdown("#### Top 5 — Atacar primero")
    top5 = df_patros.nlargest(5, "score")
    for _, row in top5.iterrows():
        with st.expander(f"{row['nombre']}  |  {row['tier_sugerido']}  |  {row['rango_precio_objetivo']}"):
            st.write(f"**Por que?** {row['nota']}")
            if row['contacto_marketing']:
                st.write(f"**Contacto:** {row['contacto_marketing']}")

with tab2:
    st.markdown("### Cervecerias — Vendor Spots")
    st.caption("Precio objetivo: $5,000 – $20,000 MXN por vendor")
    st.info("Pendiente: registrarse en https://untappd.com/api/register (gratis) y agregar credenciales.")
    st.markdown("""
    **Una vez configurado este modulo entregara:**
    - Lista de cervecerías artesanales en Mexico con rating Untappd
    - Score de prioridad por numero de check-ins, calidad y ubicacion
    - Contacto directo (Instagram, web, email)
    - Separacion automatica: leads nuevos vs. renovaciones de EBF anteriores
    """)
    st.code("""# Pasos para activar:
# 1. Ir a: https://untappd.com/api/register
# 2. Abrir config.py y agregar:
UNTAPPD_CLIENT_ID     = "tu_client_id"
UNTAPPD_CLIENT_SECRET = "tu_client_secret"
# 3. Hacer push a GitHub — el modulo se activa automaticamente""")

with tab3:
    st.markdown("### Resumen Ejecutivo — EBF Sales Pipeline")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Distribucion por Tier")
        tier_dist = df_patros["tier_sugerido"].value_counts().reset_index()
        tier_dist.columns = ["Tier", "Cantidad"]
        rangos_est = {"PREMIER": 400_000, "NAMING": 190_000, "OFICIAL": 80_000, "STAND": 30_000}
        tier_dist["Valor estimado MXN"] = tier_dist["Tier"].map(rangos_est)
        tier_dist["Pipeline total MXN"] = tier_dist["Cantidad"] * tier_dist["Valor estimado MXN"]
        st.dataframe(tier_dist, use_container_width=True, hide_index=True)
        total_pipeline = tier_dist["Pipeline total MXN"].sum()
        st.metric("Pipeline total estimado", f"${total_pipeline:,.0f} MXN")

    with col_b:
        st.markdown("#### Distribucion por Categoria")
        cat_dist = df_patros["categoria"].value_counts().reset_index()
        cat_dist.columns = ["Categoria", "Prospectos"]
        st.dataframe(cat_dist, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Roadmap del Scraper")
    roadmap = pd.DataFrame({
        "Modulo": ["A - Cervecerias", "B - Entusiastas/Homebrewers", "C - Talleres y Escuelas", "D - Patrocinadores y Marcas"],
        "Estado": ["Pendiente API Untappd", "En construccion", "En construccion", "ACTIVO — 22 leads ALTA"],
        "Objetivo de venta": ["Vendor spots $5k–$20k MXN", "Boletos $300–$1,500 MXN", "Espacio taller $3k–$8k MXN", "Patrocinios $15k–$500k+ MXN"],
        "Leads detectados": [0, 0, 0, 22],
    })
    st.table(roadmap)
