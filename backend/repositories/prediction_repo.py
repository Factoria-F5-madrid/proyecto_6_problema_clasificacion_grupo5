# backend/repositories/prediction_repo.py
from backend.db.database import AsyncSessionLocal
from backend.models.database_passenger_models import AirlinePassengerSatisfaction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
import json

async def save_prediction(payload: dict, label: str, proba: float, model_version: str):
    async with AsyncSessionLocal() as session:
        record = AirlinePassengerSatisfaction(
            passenger_id=payload.get("passenger_id"),
            gender=payload.get("gender"),
            age=payload.get("age"),
            type_of_travel=payload.get("type_of_travel"),
            inflight_wifi_service=payload.get("inflight_wifi_service"),
            customer_type=payload.get("customer_type"),
            online_boarding=payload.get("online_boarding"),
            checkin_service=payload.get("checkin_service"),
            baggage_handling=payload.get("baggage_handling"),
            seat_comfort=payload.get("seat_comfort"),
            inflight_service=payload.get("inflight_service"),
            cleanliness=payload.get("cleanliness"),
            class_type=payload.get("class_type"),
            satisfaction=label,
            features_json=json.dumps(payload),
            model_version=model_version,
        )
        session.add(record)
        await session.commit()
