# backend/repositories/prediction_repo.py
import json
from backend.db.database import AsyncSessionLocal
from backend.models.database_passenger_models import AirlinePassengerSatisfaction

async def save_prediction(input_data: dict, predicted_label: str, predicted_proba: float = None, model_version: str = None):
    """
    Safe function that creates its own AsyncSession and persists the record.
    Useful to call from background tasks.
    """
    async with AsyncSessionLocal() as session:
        rec = AirlinePassengerSatisfaction(
            passenger_id = input_data.get("passenger_id"),
            gender = input_data.get("gender"),
            customer_type = input_data.get("customer_type"),
            age = input_data.get("age"),
            class_type = input_data.get("class"),
            flight_distance = input_data.get("flight_distance"),
            departure_delay = input_data.get("departure_delay"),
            arrival_delay = input_data.get("arrival_delay"),
            seat_comfort = input_data.get("seat_comfort"),
            food_and_drink = input_data.get("food_and_drink"),
            inflight_entertainment = input_data.get("inflight_entertainment"),
            cleanliness = input_data.get("cleanliness"),
            baggage_handling = input_data.get("baggage_handling"),
            checkin_service = input_data.get("checkin_service"),
            satisfaction = predicted_label,
            features_json = json.dumps(input_data),
            model_version = model_version
        )
        session.add(rec)
        await session.commit()
        await session.refresh(rec)
        return rec
