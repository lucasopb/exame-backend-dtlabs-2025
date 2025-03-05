from sqlalchemy import Column, String, Float, DateTime
from app.models.database import Base
import ulid


class SensorData(Base):
    __tablename__ = "sensor_data"

    sensor_ulid = Column(String, primary_key=True, index=True, default=lambda: str(ulid.new()))
    server_ulid = Column(String, index=True)
    timestamp = Column(DateTime)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
