### models/mascota.py
from pydantic import BaseModel
from typing import Optional
class Mascota(BaseModel):
    id: Optional[int] = None    
    nombre: str
    rareza: str
    imagen_url: str
    lat: float
    lon: float

class MascotaActualizar(BaseModel):
    nombre: str
    rareza: str
    imagen_url: str
    lat: float
    lon: float

class MascotaPersonalizadaInput(BaseModel):
    nombre: str
    ubicacion: str
    lat: Optional[float] = None
    lon: Optional[float] = None

class MascotaConDistancia(Mascota):
    distancia_km: float
