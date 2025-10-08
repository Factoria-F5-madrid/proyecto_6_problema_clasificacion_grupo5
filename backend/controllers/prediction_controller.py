# backend/controllers/prediction_controller.py
import asyncio
from fastapi import APIRouter, Request, HTTPException
from schema.passenger_schema import PassengerInput, PredictionResponse
from repositories.prediction_repo import save_prediction

router = APIRouter()

def preprocess_input(payload: dict) -> list:
    """
    Convert input dict to model-ready feature vector.
    IMPORTANT: implement your exact preprocessing here (encoders, scalers, column order).
    This is a simple placeholder.
    """
    features = [
        payload.get("age") or 0,
        payload.get("flight_distance") or 0.0,
        payload.get("departure_delay") or 0.0,
        payload.get("arrival_delay") or 0.0,
        payload.get("seat_comfort") or 0.0,
        payload.get("food_and_drink") or 0.0,
        payload.get("inflight_entertainment") or 0.0,
        payload.get("cleanliness") or 0.0,
        payload.get("baggage_handling") or 0.0,
        payload.get("checkin_service") or 0.0
    ]
    return features

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

    # 1. Preprocess
    try:
        features = preprocess_input(payload.dict(by_alias=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {e}")

    # 2. Predict
    try:
        predicted_label, predicted_proba = predict_with_model(app, features)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    model_version = getattr(app.state, "model_version", None)

    # 3. Persist in background (don't block response)
    # schedule an async task in event loop
    asyncio.create_task(
        save_prediction(payload.dict(by_alias=True), predicted_label, predicted_proba, model_version)
    )

    return PredictionResponse(predicted_label=predicted_label, predicted_proba=predicted_proba, model_version=model_version)
