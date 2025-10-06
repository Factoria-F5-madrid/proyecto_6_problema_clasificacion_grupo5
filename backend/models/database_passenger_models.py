from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from db.database import Base
from .enums import SqlGenderTypeEnum, SqlClassTypeEnum

class AirlinePassengerSatisfaction(Base):
    __tablename__ = "airline_passenger_satisfaction"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(String, nullable=True, index=True)

    gender = Column(SqlGenderTypeEnum, nullable=True)
    customer_type = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    class_type = Column(SqlClassTypeEnum, nullable=True)  # 'Business', 'Eco', etc.
    flight_distance = Column(Float, nullable=True)
    departure_delay = Column(Float, nullable=True)
    arrival_delay = Column(Float, nullable=True)

    seat_comfort = Column(Float, nullable=True)
    food_and_drink = Column(Float, nullable=True)
    inflight_entertainment = Column(Float, nullable=True)
    cleanliness = Column(Float, nullable=True)
    baggage_handling = Column(Float, nullable=True)
    checkin_service = Column(Float, nullable=True)
    
    satisfaction = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)