# main.py
import streamlit as st
import pandas as pd
import altair as alt
import json
from pathlib import Path
import joblib  # necesario solo si cargas modelo real
import numpy as np

st.set_page_config(page_title="Clasificación - Demo", layout="wide")

# ---------------------------
# CONFIG: selecciona Mock o Real
# ---------------------------
USE_MOCK = True   # False si tienes un modelo real en /models/model.joblib
MODEL_PATH = Path("models/model.joblib")  # si te pasan un modelo, ponlo en /models

# ---------------------------
# CSS básico (opcional)
# ---------------------------
CSS = """
<style>
.card {
  background: #ffffff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 6px rgba(16,24,40,0.06);
}
.hero-title { font-size:28px; font-weight:700; margin:0; }
.hero-sub { color:#475569; margin-top:6px; margin-bottom:12px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------
# Helpers: carga dataset para EDA
# ---------------------------
DATA_PATH = Path("data/airline_passenger_satisfaction.csv")  # ajusta a tu dataset


@st.cache_data
def load_dataset(path=DATA_PATH):
    if not path.exists():
        return None
    return pd.read_csv(path)

# ---------------------------
# Helpers: predict (mock y real)
# ---------------------------
@st.cache_resource
def load_model(path=MODEL_PATH):
    try:
        return joblib.load(path)
    except Exception as e:
        st.warning("No se ha cargado ningún modelo real: " + str(e))
        return None

def mock_predict(input_dict):
    # Simula una probabilidad basada en algunas features (solo para la UI)
    base = 0.5
    if "SeatComfort" in input_dict:
        base += (int(input_dict["SeatComfort"]) - 3) * 0.06
    if "FlightDistance" in input_dict:
        base += (int(input_dict["FlightDistance"]) / 2000) * 0.05
    prob = min(max(base + np.random.normal(0, 0.05), 0.01), 0.99)
    label = "Satisfecho" if prob >= 0.5 else "No satisfecho"
    top_feats = [
        {"feature": "ServiceQuality", "importance": 0.33},
        {"feature": "SeatComfort", "importance": 0.25},
        {"feature": "OnTime", "importance": 0.12}
    ]
    return {"label": label, "probability": float(prob), "top_features": top_feats}

def real_predict(model, input_df):
    # Asume que model es un pipeline que acepta DataFrame y tiene predict_proba
    proba = model.predict_proba(input_df)[0]
    score = float(proba[1])  # prob clase positiva
    label = model.classes_[1] if hasattr(model, "classes_") else ("Positivo" if score >= 0.5 else "Negativo")
    # Intento de extraer importances
    top_feats = []
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feats = input_df.columns.tolist()
        pairs = sorted(zip(feats, importances), key=lambda x: x[1], reverse=True)[:5]
        top_feats = [{"feature": f, "importance": float(im)} for f, im in pairs]
    return {"label": label, "probability": score, "top_features": top_feats}

# ---------------------------
# Layout: Header / Hero
# ---------------------------
st.markdown("""
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;'>
  <div>
    <div class='hero-title'>Clasificación — Demo</div>
    <div class='hero-sub'>Interfaz para mostrar predicciones a partir de un dataset</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: navegación simple
page = st.sidebar.radio("Navegar", ["Home", "Predecir", "EDA", "Dashboard"])

# ---------------------------
# HOME
# ---------------------------
if page == "Home":
    st.subheader("Bienvenido")
    st.write("Esta app muestra cómo sería el frontend que consume predicciones de un modelo. Usa la pestaña *Predecir* para probar la UI.")
    st.info("Modo actual: " + ("MOCK (sin modelo)" if USE_MOCK else "REAL (cargando models/model.joblib)"))

# ---------------------------
# EDA (tú dijiste que solo hay 1 EDA)
# ---------------------------
if page == "EDA":
    st.header("Exploratory Data Analysis (EDA)")
    df = load_dataset()
    if df is None:
        st.warning("No se encontró data/dataset.csv. Coloca tu CSV allí para ver el EDA.")
    else:
        st.subheader("Muestra del dataset")
        st.dataframe(df.head(200))

        st.subheader("Descriptivos")
        st.write(df.describe(include='all').T)

        st.subheader("Distribución de una columna numérica ejemplo")
        # escoge una columna numérica si existe
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols:
            col = st.selectbox("Selecciona columna numérica", num_cols)
            chart = alt.Chart(df).mark_bar().encode(
                alt.X(f"{col}:Q", bin=alt.Bin(maxbins=30)),
                y='count()'
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No hay columnas numéricas en el dataset.")

# ---------------------------
# PREDICT (formulario + resultado)
# ---------------------------
if page == "Predecir":
    st.header("Formulario de entrada")
    st.markdown("Rellena los campos y comprueba la predicción (interfaz).")

    # Form: ajusta los campos a los que tiene tu dataset/modelo
    with st.form("input_form"):
        age = st.number_input("Edad", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Género", ["Male", "Female", "Other"])
        flight_distance = st.number_input("Flight distance", min_value=0, value=500)
        seat_comfort = st.slider("Seat comfort (1-5)", 1,5,3)
        submitted = st.form_submit_button("Predecir")

    if submitted:
        input_dict = {
            "Age": age,
            "Gender": gender,
            "FlightDistance": flight_distance,
            "SeatComfort": seat_comfort
        }

        if USE_MOCK:
            res = mock_predict(input_dict)
        else:
            model = load_model()
            if model is None:
                st.error("No hay modelo cargado en models/model.joblib. Cambia a USE_MOCK=True si no tienes modelo.")
                st.stop()
            # convertir a DataFrame con columnas en el orden esperado
            df_input = pd.DataFrame([input_dict])
            res = real_predict(model, df_input)

        # Mostrar resultado en una tarjeta
        st.markdown(f"""
        <div class='card' style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-size:14px;color:#666;">Predicción</div>
            <div style="font-size:18px;font-weight:700;">{res['label']}</div>
            <div style="font-size:13px;color:#666;">Probabilidad: {(res['probability']*100):.0f}%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Gráfico top features (Altair)
        if res.get("top_features"):
            df_feats = pd.DataFrame(res["top_features"])
            chart = alt.Chart(df_feats).mark_bar().encode(
                x=alt.X("importance:Q", title="Importancia"),
                y=alt.Y("feature:N", sort='-x', title=None)
            ).properties(height=180)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No hay importancias disponibles para este modelo.")

# ---------------------------
# DASHBOARD (métricas guardadas)
# ---------------------------
if page == "Dashboard":
    st.header("Dashboard técnico")
    metrics_path = Path("models/metrics.json")
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding='utf-8'))
        st.metric("Accuracy (val)", metrics.get("val", {}).get("accuracy", "—"))
        st.metric("F1 (val)", metrics.get("val", {}).get("f1", "—"))
        # matriz de confusión si existe
        if metrics.get("confusion_matrix"):
            import plotly.express as px
            cm = metrics["confusion_matrix"]
            fig = px.imshow(cm, text_auto=True, labels=dict(x="Pred", y="True"))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No se encontró models/metrics.json. Pide al equipo que lo genere con las métricas de evaluación.")
