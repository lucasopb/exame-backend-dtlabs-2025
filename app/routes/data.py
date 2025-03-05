from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.sensor import SensorDataSchema
from typing import Optional
from app.services.data_service import register_sensor_data, get_sensor_data
from app.api.dependencies import get_current_user  
from app.models.user import User  

router = APIRouter()

@router.post("/data", response_model=SensorDataSchema)
def register_sensor_data_route(sensor_data: SensorDataSchema, db: Session = Depends(get_db)):
    try:
        sensor_record = register_sensor_data(sensor_data, db)
        return sensor_record
    except HTTPException as e:
        raise e

@router.get("/data")
def get_sensor_data_route(
    db: Session = Depends(get_db),
    server_ulid: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    sensor_type: Optional[str] = None,
    aggregation: Optional[str] = None,
):
    try:
        data = get_sensor_data(db, server_ulid, start_time, end_time, sensor_type, aggregation)
        return data
    except HTTPException as e:
        raise e