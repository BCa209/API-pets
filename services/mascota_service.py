import random
from models.mascota import Mascota
from models.mascota_sqlite import MascotaDB
from services.generador_coordenadas import generar_coordenada_dentro_de_radio
from data.ciudades import CIUDADES
from data.puntos import PUNTOS
from services.moldes_service import obtener_moldes_mascotas
#from services.mascota_spawn import generar_mascotas
from services.db_service import (
    init_db,
    eliminar_mascotas_por_ubicacion as eliminar_db_mascotas,
    guardar_mascotas_en_db,
    obtener_mascotas_por_ubicacion,
    actualizar_mascota_en_db,
)

def generar_mascotas(ubicacion: str, tipo: str, cantidad: int = 5) -> list[Mascota]:
    datos = CIUDADES.get(ubicacion) if tipo == "ciudad" else PUNTOS.get(ubicacion)
    if not datos:
        return []

    moldes = obtener_moldes_mascotas()
    if not moldes:
        return []

    mascotas = []
    mascotas_db = []

    for _ in range(cantidad):
        molde = random.choices(
            population=moldes,
            weights=[probabilidad_por_rareza(m["rareza"]) for m in moldes],
            k=1
        )[0]
        lat, lon = generar_coordenada_dentro_de_radio(datos["centro"], datos["radio_km"])

        mascota_db = MascotaDB(
            nombre=molde["nombre"],
            rareza=molde["rareza"],
            imagen_url=molde["imagen_url"],
            lat=lat,
            lon=lon,
            ubicacion=ubicacion
        )
        mascotas_db.append(mascota_db)

    guardar_mascotas_en_db(mascotas_db)

    # Volver a consultarlas para obtener los IDs autogenerados
    return obtener_mascotas_por_ubicacion(ubicacion)

def probabilidad_por_rareza(rareza: str) -> float:
    probabilidades = {
        "común": 0.25,
        "raro": 0.25,
        "ultra raro": 0.25,
        "legendario": 0.25
    }
    return probabilidades.get(rareza.lower(), 0.1)

# Agregar mascotas en una ubicación (para POST)
def crear_mascotas_en_ubicacion(ubicacion: str, tipo: str, cantidad: int = 5) -> list[Mascota]:
    return generar_mascotas(ubicacion, tipo, cantidad)

# Reemplazar mascotas en una ubicación (para POST)
def reiniciar_mascotas_en_ubicacion(ubicacion: str, tipo: str, cantidad: int = 5) -> list[Mascota]:
    eliminar_mascotas_por_ubicacion(ubicacion)
    return generar_mascotas(ubicacion, tipo, cantidad)

# Eliminar mascotas por ubicación (para DELETE)
def eliminar_mascotas_por_ubicacion(ubicacion: str) -> int:
    return eliminar_db_mascotas(ubicacion)

#agregar insercion 1x1 existente
def agregar_mascota_existente(nombre: str, ubicacion: str, lat: float | None = None, lon: float | None = None) -> Mascota | None:
    moldes = obtener_moldes_mascotas()
    molde = next((m for m in moldes if m["nombre"].lower() == nombre.lower()), None)

    if not molde:
        return None

    datos = CIUDADES.get(ubicacion) or PUNTOS.get(ubicacion)
    if not datos:
        return None

    if lat is None or lon is None:
        lat, lon = generar_coordenada_dentro_de_radio(datos["centro"], datos["radio_km"])

    mascota = Mascota(
        nombre=molde["nombre"],
        rareza=molde["rareza"],
        imagen_url=molde["imagen_url"],
        lat=lat,
        lon=lon
    )

    mascota_db = MascotaDB(
        nombre=mascota.nombre,
        rareza=mascota.rareza,
        imagen_url=mascota.imagen_url,
        lat=mascota.lat,
        lon=mascota.lon,
        ubicacion=ubicacion
    )

    guardar_mascotas_en_db([mascota_db])

    return mascota
