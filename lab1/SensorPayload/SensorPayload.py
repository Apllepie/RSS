from pydantic import BaseModel

class SensorPayload(BaseModel):
    sensor_name: str
    value: float