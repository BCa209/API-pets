from fastapi import APIRouter, Query, Body, HTTPException
from models.mascota import Mascota, MascotaActualizar, MascotaPersonalizadaInput
from services.db_service import (
    actualizar_mascota_en_db, 
    obtener_todas_las_mascotas,
    eliminar_mascota_por_coordenadas
)
from services.mascota_service import (
    reiniciar_mascotas_en_ubicacion,
    eliminar_mascotas_por_ubicacion,
    obtener_mascotas_por_ubicacion,
    crear_mascotas_en_ubicacion,
    agregar_mascota_existente
)

router = APIRouter()

# Obtener TODAS las mascotas de la base de datos
@router.get("/mascotas/todos", response_model=list[Mascota])
def obtener_todas_las_mascotas_endpoint():
    return obtener_todas_las_mascotas()

# Obtener mascotas (si existen ya guardadas, no regenera)
@router.get("/mascotas", response_model=list[Mascota])
def obtener_mascotas(
    ubicacion: str = Query(...),
    tipo: str = Query("ciudad"),
    cantidad: int = Query(5)
):
    existentes = obtener_mascotas_por_ubicacion(ubicacion)
    if existentes:
        return existentes
    # Mascotas no encontradas
    raise HTTPException(status_code=404, detail=f"No se encontraron mascotas en '{ubicacion}'")

# Generar mascotas (agrega nuevas sin borrar las existentes)
@router.post("/mascotas/spawn", response_model=list[Mascota])
def spawn_mascotas(
    ubicacion: str = Query(...),
    tipo: str = Query("ciudad"),
    cantidad: int = Query(5)
):
    return crear_mascotas_en_ubicacion(ubicacion, tipo, cantidad)

# Regenerar mascotas (elimina las actuales y crea nuevas)
@router.post("/mascotas/regenerar", response_model=list[Mascota])
def regenerar_mascotas(
    ubicacion: str = Query(...),
    tipo: str = Query("ciudad"),
    cantidad: int = Query(5)
):
    eliminar_mascotas_por_ubicacion(ubicacion)
    return reiniciar_mascotas_en_ubicacion(ubicacion, tipo, cantidad)

# Eliminar mascotas existentes de una ubicación
@router.delete("/mascotas")
def borrar_mascotas(
    ubicacion: str = Query(...)
):
    eliminar_mascotas_por_ubicacion(ubicacion)
    return {"mensaje": f"Mascotas en '{ubicacion}' eliminadas correctamente"}

# Actualizar una mascota por ID
@router.put("/mascotas/{id}", response_model=Mascota)
def actualizar_mascota(id: int, datos_actualizados: MascotaActualizar = Body(...)):
    mascota = actualizar_mascota_en_db(id, datos_actualizados)
    if mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

# Agregar una nueva mascota a partir de un molde
@router.post("/mascotas/existente", response_model=Mascota)
def agregar_mascota_personalizada_endpoint(data: MascotaPersonalizadaInput = Body(...)):
    mascota = agregar_mascota_existente(
        nombre=data.nombre,
        ubicacion=data.ubicacion,
        lat=data.lat,
        lon=data.lon
    )
    if mascota is None:
        raise HTTPException(status_code=404, detail="Molde no encontrado o ubicación inválida")
    return mascota

# Eliminar mascotas por coordenadas (latitud y longitud)
@router.delete("/mascotas/ubicacion")
def eliminar_mascota_por_ubicacion(
    lat: float = Query(...),
    lon: float = Query(...)
):
    eliminadas = eliminar_mascota_por_coordenadas(lat, lon)
    if eliminadas == 0:
        raise HTTPException(status_code=404, detail="Mascota no encontrada con esas coordenadas")
    return {"mensaje": f"Mascota eliminada correctamente (lat: {lat}, lon: {lon})"}