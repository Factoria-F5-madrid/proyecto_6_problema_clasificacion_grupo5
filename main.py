# main.py
import streamlit as st
from src import ui
from pathlib import Path

st.set_page_config(page_title="Experience the World", layout="wide", initial_sidebar_state="collapsed")

# Carga CSS (estilo separado)
ui.inject_css("assets/styles.css")

# Top navigation; devuelve la página actual (session_state.page)
page = ui.top_nav(logo_path="assets/logo.svg", nav_items=["Home","Predecir","EDA","Dashboard"])

# Solo mostramos Home: hero con tu texto y botón
if page == "Home":
    ui.hero_block(
        title="Experience the World",
        subtitle="from Above",
        desc="Explore premium flight experiences designed to elevate your travel to new heights."
    )

# Minimal: si navegas a Predecir mostramos un placeholder (tu frontend real va aquí)
if page == "Predecir":
    st.header("Predecir - Aquí irá el formulario de predicción")
    st.write("En este proyecto tu equipo de ML te puede dar model.joblib y aquí se integrará.")

# EDA / Dashboard placeholders para no romper la navegación
if page == "EDA":
    st.header("EDA")
    st.write("Coloca data/dataset.csv en /data para mostrar EDA si lo necesitas.")

if page == "Dashboard":
    st.header("Dashboard")
    st.write("Métricas del modelo aparecerán aquí cuando estén disponibles.")
    st.write("Puedes usar Altair o Plotly para gráficos interactivos.")