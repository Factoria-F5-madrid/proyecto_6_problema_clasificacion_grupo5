# backend/controllers/prediction_controller.py
import asyncio
from fastapi import APIRouter, Request, HTTPException
from backend.schema.passenger_schema import PassengerInput, PredictionResponse
from backend.repositories.prediction_repo import save_prediction

router = APIRouter()

# 🔢 Ajusta este orden al feature_order del modelo entrenado
FEATURE_ORDER = [
    "type_of_travel",
    "inflight_wifi_service",
    "customer_type",
    "online_boarding",
    "checkin_service",
    "baggage_handling",
    "seat_comfort",
    "inflight_service",
    "cleanliness",
    "class_type"
]

def preprocess_input(payload: dict) -> list:
    """
    Extrae las features en el orden exacto esperado por el modelo.
    Si tu modelo fue entrenado con variables numéricas, convierte los valores categóricos.
    """
    def encode_value(val):
        if isinstance(val, str):
            val_lower = val.strip().lower()
            mapping = {
                "male": 0,
                "female": 1,
                "business travel": 1,
                "personal travel": 0,
                "loyal customer": 1,
                "disloyal customer": 0,
                "eco": 0,
                "eco plus": 1,
                "business": 2
            }
            return mapping.get(val_lower, 0.0)
        return val or 0.0

    return [encode_value(payload.get(f)) for f in FEATURE_ORDER]

def predict_with_model(app, features):
    model = app.state.model
    if model is None:
        raise RuntimeError("ML model not loaded.")
    try:
        y_pred = model.predict([features])
    except Exception as e:
        raise RuntimeError(f"Model predict error: {e}")

    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba_arr = model.predict_proba([features])
            proba = float(max(proba_arr[0]))
        except Exception:
            proba = None

    return str(y_pred[0]), proba

@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(payload: PassengerInput, request: Request):
    app = request.app

    # 1️⃣ Preprocess
    try:
        features = preprocess_input(payload.dict(by_alias=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {e}")

    # 2️⃣ Predict
    try:
        predicted_label, predicted_proba = predict_with_model(app, features)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    model_version = getattr(app.state, "model_version", None)

    # 3️⃣ Save asynchronously
    asyncio.create_task(
        save_prediction(payload.dict(by_alias=True), predicted_label, predicted_proba, model_version)
    )

    label_mapping = {
        0: "neutral or dissatisfied",
        1: "satisfied"
    }

    return PredictionResponse(
        predicted_label=predicted_label,
        satisfaction=label_mapping.get(int(predicted_label), "Unknown"),
        predicted_proba=predicted_proba,
        model_version=model_version
    )
