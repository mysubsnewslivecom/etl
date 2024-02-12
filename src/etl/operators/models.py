from pydantic import BaseModel


class ISSLocationModel(BaseModel):
    latitude: float
    longitude: float
    location_timestamp: int
