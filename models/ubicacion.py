from pydantic import BaseModel

class Coordenadas(BaseModel):
    lat: float
    lon: float
