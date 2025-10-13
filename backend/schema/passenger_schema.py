# backend/schema/airline_passenger_satisfaction_schema.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Union

from sqlalchemy import DateTime
from backend.models.enums import GenderTypeEnum, class_type_enum

class PassengerInput(BaseModel):
    passenger_id: Optional[str] = Field(None, example="P0001")
    gender: Optional[str] = Field(None, example="male")
    age: Optional[int] = Field(None, example=29)

    # ✅ Las 10 features usadas por el modelo
    inflight_wifi_service: Optional[float] = Field(None, example=4)
    online_boarding: Optional[float] = Field(None, example=5)
    checkin_service: Optional[float] = Field(None, example=4)
    baggage_handling: Optional[float] = Field(None, example=5)
    seat_comfort: Optional[float] = Field(None, example=4)
    inflight_service: Optional[float] = Field(None, example=5)
    cleanliness: Optional[float] = Field(None, example=4)
    type_of_travel: Optional[str] = Field(None, example="Business travel")
    customer_type: Optional[str] = Field(None, example="Loyal Customer")
    class_type: Optional[str] = Field(None, example="Eco Plus")

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
                "inflight_wifi_service": 4,
                "online_boarding": 5,
                "checkin_service": 4,
                "baggage_handling": 5,
                "seat_comfort": 4,
                "inflight_service": 5,
                "cleanliness": 4,
                "type_of_travel": "Business travel",
                "class_type": "Economy Plus"
                
            }
        }

class PredictionResponse(BaseModel):
    predicted_label: str
    satisfaction: Optional[str]
    predicted_proba: Optional[float]
    model_version: Optional[str]
