# backend/models/database_passenger_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from backend.db.database import Base
from .enums import SqlGenderTypeEnum, SqlClassTypeEnum

class AirlinePassengerSatisfaction(Base):
    __tablename__ = "airline_passenger_satisfaction"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(String, nullable=True, index=True)

    gender = Column(SqlGenderTypeEnum, nullable=True)
    customer_type = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    type_of_travel = Column(String, nullable=True)
    class_type = Column(SqlClassTypeEnum, nullable=True)

    flight_distance = Column(Float, nullable=True)
    inflight_wifi_service = Column(Float, nullable=True)
    departure_arrival_time_convenient = Column(Float, nullable=True)
    ease_of_online_booking = Column(Float, nullable=True)
    gate_location = Column(Float, nullable=True)
    food_and_drink = Column(Float, nullable=True)
    online_boarding = Column(Float, nullable=True)
    seat_comfort = Column(Float, nullable=True)
    inflight_entertainment = Column(Float, nullable=True)
    on_board_service = Column(Float, nullable=True)
    leg_room_service = Column(Float, nullable=True)
    baggage_handling = Column(Float, nullable=True)
    checkin_service = Column(Float, nullable=True)
    inflight_service = Column(Float, nullable=True)
    cleanliness = Column(Float, nullable=True)

    departure_delay_minutes = Column(Float, nullable=True)
    arrival_delay_minutes = Column(Float, nullable=True)

    satisfaction = Column(String, nullable=True)
    features_json = Column(Text, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
