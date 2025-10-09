# backend/schema/airline_passenger_satisfaction_schema.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Union

from sqlalchemy import DateTime
from backend.models.enums import GenderTypeEnum, class_type_enum

class PassengerInput(BaseModel):
    passenger_id: Optional[str] = None
    gender: Union[GenderTypeEnum, str]
    customer_type: Optional[str] = None
    age: Optional[int] = None
    class_type: Union[class_type_enum, str] = Field(None, alias="class")
    flight_distance: Optional[float] = None
    departure_delay: Optional[float] = None
    arrival_delay: Optional[float] = None

    seat_comfort: Optional[float] = None
    food_and_drink: Optional[float] = None
    inflight_entertainment: Optional[float] = None
    cleanliness: Optional[float] = None
    baggage_handling: Optional[float] = None
    checkin_service: Optional[float] = None

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
                "passenger_id": "pax_123",
                "gender": "Male",
                "customer_type": "Loyal Customer",
                "age": 34,
                "class": "Economy",
                "flight_distance": 500,
                "departure_delay": 10,
                "arrival_delay": 5,
                "seat_comfort": 4.0,
                "food_and_drink": 3.0,
                "inflight_entertainment": 4.0,
                "cleanliness": 4.0,
                "baggage_handling": 3.0,
                "checkin_service": 4.0
            }
        }

class PredictionResponse(BaseModel):
    predicted_label: str
    predicted_proba: Optional[float] = None
    model_version: Optional[str] = None
