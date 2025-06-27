### services/ubicacion_service.py
import os
import json
import time
from typing import Optional
from datetime import datetime, timedelta
from geopy.distance import geodesic
from math import sqrt
from services.db_service import obtener_todas_las_mascotas
from data.puntos import PUNTOS
from data.ciudades import CIUDADES

def obtener_ubicacion_por_coordenadas(lat: float, lon: float) -> str | None:
    for nombre, datos in {**CIUDADES, **PUNTOS}.items():
        centro = datos["centro"]
        radio_km = datos["radio_km"]
        distancia = geodesic((lat, lon), centro).km
        if distancia <= radio_km:
            return nombre
    return None

TEMP_DIR = "temp_data/ubicaciones_id_telefono"
MAX_TIEMPO_SEGUNDOS = 2 * 3600          #2horas

def _get_path(id_telefono: str) -> str:
    return os.path.join(TEMP_DIR, f"{id_telefono}.json")

def guardar_ubicacion(id_telefono: str, lat: float, lon: float):
    ahora = time.time()
    path = _get_path(id_telefono)

    datos = []
    if os.path.exists(path):
        with open(path, "r") as f:
            datos = json.load(f)

    # Filtrar ubicaciones anteriores válidas
    datos = [d for d in datos if ahora - d["timestamp"] <= MAX_TIEMPO_SEGUNDOS]

    # Agregar nueva ubicación
    datos.append({
        "lat": lat,
        "lon": lon,
        "timestamp": ahora
    })

    with open(path, "w") as f:
        json.dump(datos, f)

def obtener_ultima_ubicacion(id_telefono: str) -> Optional[dict]:
    path = _get_path(id_telefono)
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        datos = json.load(f)

    if not datos:
        return None

    # Última ubicación válida
    datos = [d for d in datos if time.time() - d["timestamp"] <= MAX_TIEMPO_SEGUNDOS]
    return datos[-1] if datos else None

def obtener_mascotas_ordenadas_por_distancia(id_telefono: str, orden: str = "asc") -> list:
    ubicacion = obtener_ultima_ubicacion(id_telefono)
    if not ubicacion:
        return []

    lat0, lon0 = ubicacion["lat"], ubicacion["lon"]
    mascotas = obtener_todas_las_mascotas()

    mascotas_con_distancia = []
    for m in mascotas:
        distancia = geodesic((lat0, lon0), (m.lat, m.lon)).km
        mascota_dict = m.dict()
        mascota_dict["distancia_km"] = round(distancia, 4)
        mascotas_con_distancia.append(mascota_dict)

    mascotas_ordenadas = sorted(
        mascotas_con_distancia,
        key=lambda m: m["distancia_km"],
        reverse=(orden == "desc")
    )

    return mascotas_ordenadas
