# backend/models/database_passenger_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from backend.db.database import Base
from .enums import SqlGenderTypeEnum, SqlClassTypeEnum, SqlCustomerType, SqlTypeOfTravel

class AirlinePassengerSatisfaction(Base):
    __tablename__ = "airline_passenger_satisfaction"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(String, nullable=True, index=True)

    # estos campos iran en los inputs y aunque usamos las 10 feature de debajo en el modelo e no afectara estos 2 campos en la predicción
    gender = Column(SqlGenderTypeEnum, nullable=True)
    age = Column(Integer, nullable=True)

    # las 10 features que vamos a usar (numeric where appropriate)
    type_of_travel = Column(SqlTypeOfTravel, nullable=True)
    inflight_wifi_service = Column(Float, nullable=True)
    customer_type = Column(SqlCustomerType, nullable=True)
    online_boarding = Column(Float, nullable=True)
    checkin_service = Column(Float, nullable=True)
    baggage_handling = Column(Float, nullable=True)
    seat_comfort = Column(Float, nullable=True)
    inflight_service = Column(Float, nullable=True)
    cleanliness = Column(Float, nullable=True)
    class_type = Column(SqlClassTypeEnum, nullable=True)

    # target / meta
    satisfaction = Column(String, nullable=True)
    features_json = Column(Text, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
