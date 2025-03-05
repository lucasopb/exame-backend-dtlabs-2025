from sqlalchemy.orm import Session
from app.models.sensor import SensorData
from app.schemas.sensor import SensorDataSchema
from fastapi import HTTPException
from app.models.server import Server
from typing import Optional
from sqlalchemy.sql import func
from datetime import datetime
from threading import Timer


def register_sensor_data(sensor_data: SensorDataSchema, db: Session):
    server = db.query(Server).filter(Server.server_ulid == sensor_data.server_ulid).first()
    if not server:
        raise HTTPException(status_code=400, detail="Server ULID not found.")

    if all([sensor_data.temperature is None, sensor_data.humidity is None, sensor_data.voltage is None, sensor_data.current is None]):
        raise HTTPException(status_code=400, detail="At least one sensor value must be provided.")

    sensor_record = SensorData(
        server_ulid=sensor_data.server_ulid,
        timestamp=sensor_data.timestamp,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity,
        voltage=sensor_data.voltage,
        current=sensor_data.current
    )
    
    db.add(sensor_record)
    db.commit()
    db.refresh(sensor_record)

    #Set server online
    server.is_online = True
    db.commit()
    
    #Set server offline after 10 secunds
    def set_server_offline(db: Session, server_ulid: str):
        server = db.query(Server).filter(Server.server_ulid == server_ulid).first()
        if server:
            server.is_online = False
            db.commit()

    def schedule_set_offline(db: Session, server_ulid: str):
        Timer(10, set_server_offline, [db, server_ulid]).start()

    schedule_set_offline(db, server.server_ulid)

    return sensor_record


def get_sensor_data(
    db: Session,
    server_ulid: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    sensor_type: Optional[str] = None,
    aggregation: Optional[str] = None
):
    query = db.query(SensorData)

    if server_ulid:
        query = query.filter(SensorData.server_ulid == server_ulid)
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time)
            query = query.filter(SensorData.timestamp >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_time format. Use ISO 8601.")

    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time)
            query = query.filter(SensorData.timestamp <= end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_time format. Use ISO 8601.")

    if sensor_type and sensor_type not in ["temperature", "humidity", "voltage", "current"]:
        raise HTTPException(status_code=400, detail="Invalid sensor_type. Must be one of: temperature, humidity, voltage, current.")

    if aggregation:
        if aggregation not in ["minute", "hour", "day"]:
            raise HTTPException(status_code=400, detail="Invalid aggregation. Must be one of: minute, hour, day.")

        interval_map = {
            "minute": "%Y-%m-%d %H:%M:00",
            "hour": "%Y-%m-%d %H:00:00",
            "day": "%Y-%m-%d 00:00:00"
        }
        time_format = interval_map[aggregation]

        aggregation_query = db.query(
            func.strftime(time_format, SensorData.timestamp).label("timestamp"),
            func.avg(SensorData.temperature).label("temperature"),
            func.avg(SensorData.humidity).label("humidity"),
            func.avg(SensorData.voltage).label("voltage"),
            func.avg(SensorData.current).label("current")
        )

        # Aplicar os mesmos filtros na agregação
        if server_ulid:
            aggregation_query = aggregation_query.filter(SensorData.server_ulid == server_ulid)
        if start_time:
            aggregation_query = aggregation_query.filter(SensorData.timestamp >= start_dt)
        if end_time:
            aggregation_query = aggregation_query.filter(SensorData.timestamp <= end_dt)

        aggregation_query = aggregation_query.group_by(func.strftime(time_format, SensorData.timestamp))
        results = aggregation_query.all()

    else:
        results = query.all()

    response = []
    for row in results:
        data_entry = {
            "timestamp": row.timestamp,
        }
        if sensor_type:
            data_entry[sensor_type] = getattr(row, sensor_type)
        else:
            if row.temperature is not None:
                data_entry["temperature"] = row.temperature
            if row.humidity is not None:
                data_entry["humidity"] = row.humidity
            if row.voltage is not None:
                data_entry["voltage"] = row.voltage
            if row.current is not None:
                data_entry["current"] = row.current
        
        response.append(data_entry)

    return response
