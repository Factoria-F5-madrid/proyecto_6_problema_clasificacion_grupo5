# src/ui.py
import streamlit as st

def inject_css(path="assets/styles.css"):
    """Carga CSS desde assets/styles.css (silencioso si no existe)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # no fallar si falta css
        st.warning("assets/styles.css no encontrada. Añádela para el estilo completo.")

def top_nav(logo_path="assets/logo.svg", nav_items=None):
    """Dibuja topnav. Usa st.session_state.page como manejo de página."""
    if nav_items is None:
        nav_items = ["Home", "Predecir", "Dashboard"]

    # asegurar page en session_state
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # HTML para la barra (visual). Los botones reales son Streamlit buttons alineados a la derecha.
    st.markdown(f"""
    <div class="topnav">
      <div class="brand">
        <img src="{logo_path}" alt="logo" />
      </div>
      <div class="nav-links">
        <div style="display:flex; gap:18px; align-items:center;">
          <span class="nav-item">Home</span>
          <span class="nav-item">Predecir</span>
          <span class="nav-item">EDA</span>
          <span class="nav-item">Dashboard</span>
        </div>
      </div>
      <div style="display:flex; gap:8px; align-items:center;">
        <div>
          <button class="nav-cta" onclick="window.scrollTo(0,document.body.scrollHeight)">Book Now</button>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # fallback con streamlit buttons para navegación funcional
    cols = st.columns([1,1,1,1])
    labels = nav_items[:4]
    for i, lbl in enumerate(labels):
        if cols[i].button(lbl):
            st.session_state.page = lbl

    return st.session_state.page

def hero_block(title, subtitle, desc, cta_label="Book Your Flight Now"):
    """Renderiza el bloque central con el texto y el CTA grande."""
    st.markdown('<div class="hero-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="hero-center">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="hero-title">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="hero-sub">{subtitle}</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-desc">{desc}</div>', unsafe_allow_html=True)
    # CTA: usar un botón streamlit, pero con clase visual hero-cta (estilizado por CSS)
    if st.button(cta_label, key="hero_cta"):
        st.session_state.page = "Predecir"
    # añadir un separador visual y cierre de contenedores
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-separator"></div>', unsafe_allow_html=True)