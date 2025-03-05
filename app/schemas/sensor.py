from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SensorDataSchema(BaseModel):
    server_ulid: str
    timestamp: datetime
    temperature: Optional[float] = Field(None, ge=-50, le=100, description="Temperatura em °C")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Umidade relativa em %")
    voltage: Optional[float] = Field(None, ge=0, description="Tensão elétrica em Volts")
    current: Optional[float] = Field(None, ge=0, description="Corrente elétrica em Ampères")

    class Config:
        orm_mode = True
