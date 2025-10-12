# backend/schema/airline_passenger_satisfaction_schema.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Union

from sqlalchemy import DateTime
from backend.models.enums import GenderTypeEnum, class_type_enum

class PassengerInput(BaseModel):
    passenger_id: Optional[str] = None
    gender: Optional[str] = None
    customer_type: Optional[str] = None
    age: Optional[int] = None
    type_of_travel: Optional[str] = None
    class_type: Optional[str] = Field(None, alias="class")
    flight_distance: Optional[float] = None
    inflight_wifi_service: Optional[float] = None
    departure_arrival_time_convenient: Optional[float] = None
    ease_of_online_booking: Optional[float] = None
    gate_location: Optional[float] = None
    food_and_drink: Optional[float] = None
    online_boarding: Optional[float] = None
    seat_comfort: Optional[float] = None
    inflight_entertainment: Optional[float] = None
    on_board_service: Optional[float] = None
    leg_room_service: Optional[float] = None
    baggage_handling: Optional[float] = None
    checkin_service: Optional[float] = None
    inflight_service: Optional[float] = None
    cleanliness: Optional[float] = None
    departure_delay_minutes: Optional[float] = Field(None, alias="Departure Delay in Minutes")
    arrival_delay_minutes: Optional[float] = Field(None, alias="Arrival Delay in Minutes")

    @validator("gender")
    def validate_gender(cls, value):
        if value not in GenderTypeEnum:
            raise ValueError(f"Invalid gender type: {value}")
        return value

    @validator("class_type")
    def validate_class_type(cls, value):
        if value not in class_type_enum:
            raise ValueError(f"Invalid class type: {value}")
        return value


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "passenger_id": "pax_001",
                "gender": "Male",
                "customer_type": "Loyal Customer",
                "age": 34,
                "type_of_travel": "Business travel",
                "class": "Business",
                "flight_distance": 500,
                "inflight_wifi_service": 4,
                "departure_arrival_time_convenient": 4,
                "ease_of_online_booking": 3,
                "gate_location": 3,
                "food_and_drink": 3,
                "online_boarding": 4,
                "seat_comfort": 4,
                "inflight_entertainment": 3,
                "on_board_service": 4,
                "leg_room_service": 3,
                "baggage_handling": 3,
                "checkin_service": 4,
                "inflight_service": 4,
                "cleanliness": 4,
                "Departure Delay in Minutes": 10,
                "Arrival Delay in Minutes": 5
            }
        }

class PredictionResponse(BaseModel):
    predicted_label: str
    predicted_proba: Optional[float] = None
    model_version: Optional[str] = None
