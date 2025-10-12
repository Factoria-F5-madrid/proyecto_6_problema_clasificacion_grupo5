# backend/controllers/prediction_controller.py
import asyncio
from fastapi import APIRouter, Request, HTTPException
from backend.schema.passenger_schema import PassengerInput, PredictionResponse
from backend.repositories.prediction_repo import save_prediction

router = APIRouter()

def preprocess_input(payload: dict) -> list:
    """
    Return features in the exact order used at training.
    """
    # ejemplo de orden: ajusta a tu X_train.columns
    features = [
        payload.get("gender"),
        payload.get("customer_type"),
        payload.get("age") or 0,
        payload.get("type_of_travel"),
        payload.get("class") or payload.get("class_type"),
        payload.get("flight_distance") or 0.0,
        payload.get("inflight_wifi_service") or 0.0,
        payload.get("departure_arrival_time_convenient") or 0.0,
        payload.get("ease_of_online_booking") or 0.0,
        payload.get("gate_location") or 0.0,
        payload.get("food_and_drink") or 0.0,
        payload.get("online_boarding") or 0.0,
        payload.get("seat_comfort") or 0.0,
        payload.get("inflight_entertainment") or 0.0,
        payload.get("on_board_service") or 0.0,
        payload.get("leg_room_service") or 0.0,
        payload.get("baggage_handling") or 0.0,
        payload.get("checkin_service") or 0.0,
        payload.get("inflight_service") or 0.0,
        payload.get("cleanliness") or 0.0,
        payload.get("Departure Delay in Minutes") or payload.get("departure_delay_minutes") or 0.0,
        payload.get("Arrival Delay in Minutes") or payload.get("arrival_delay_minutes") or 0.0
    ]

    # If your model expects numeric encodings for gender/class/type_of_travel -> convert here
    # But best approach: load preprocessor pipeline used in training (see below)
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
