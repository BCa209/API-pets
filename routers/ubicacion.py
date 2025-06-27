### routers/ubicacion.py

from fastapi import APIRouter, HTTPException, Query
from fastapi import Body
from math import sqrt
from models.ubicacion import Coordenadas
from models.mascota import Mascota, MascotaConDistancia
from services.ubicacion_service import (
    guardar_ubicacion,
    obtener_ubicacion_por_coordenadas, obtener_ultima_ubicacion,
    obtener_mascotas_ordenadas_por_distancia)
from services.db_service import obtener_todas_las_mascotas, obtener_todas_mascotas

router = APIRouter()

"""@router.post("/ubicacion")
def recibir_coordenadas(coord: Coordenadas):
    ubicacion = obtener_ubicacion_por_coordenadas(coord.lat, coord.lon)
    if ubicacion is None:
        raise HTTPException(status_code=404, detail="No se encontró una ubicación cercana")
    return {"ubicacion": ubicacion}"""

@router.post("/ubicacion")
def recibir_ubicacion(
    id_telefono: str = Body(...),
    lat: float = Body(...),
    lon: float = Body(...)
):
    guardar_ubicacion(id_telefono, lat, lon)
    return {"mensaje": "Ubicación guardada correctamente"}

@router.get("/mascotas/cercanas", response_model=list[Mascota])
def mascotas_cercanas(id_telefono: str):
    ubicacion = obtener_ultima_ubicacion(id_telefono)
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o expirada")

    lat0 = ubicacion["lat"]
    lon0 = ubicacion["lon"]

    mascotas = obtener_todas_mascotas()
    if not mascotas:
        return []

    # Ordenar por distancia euclidiana (puedes usar Haversine si prefieres)
    mascotas_ordenadas = sorted(
        mascotas,
        key=lambda m: sqrt((m.lat - lat0)**2 + (m.lon - lon0)**2)
    )
    return mascotas_ordenadas

@router.get("/mascotas/ordenadas", response_model=list[MascotaConDistancia])
def obtener_mascotas_ordenadas(
    id_telefono: str = Query(...),
    orden: str = Query("desc")  # Puede ser 'asc' o 'desc'
):
    mascotas = obtener_mascotas_ordenadas_por_distancia(id_telefono, orden=orden)
    if not mascotas:
        raise HTTPException(status_code=404, detail="No se encontraron mascotas o ubicación expirada")
    return mascotas