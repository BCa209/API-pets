### routers/mascotas.py
import os, shutil
from fastapi import APIRouter, Query, Body, HTTPException, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from models.mascota import Mascota, MascotaActualizar, MascotaExistenteInput, MascotaPersonalizada, MascotaOut
from services.db_service import (
    actualizar_mascota_en_db, 
    obtener_todas_las_mascotas,
    eliminar_mascota_por_coordenadas,
    get_db_session
)
from services.mascota_service import (
    reiniciar_mascotas_en_ubicacion,
    eliminar_mascotas_por_ubicacion,
    obtener_mascotas_por_ubicacion,
    crear_mascotas_en_ubicacion,
    agregar_mascota_existente,
    agregar_mascota_personalizada
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
def agregar_mascota_existente_endpoint(data: MascotaExistenteInput = Body(...)):
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

@router.post("/mascotas/personalizado", response_model=MascotaOut)
def crear_mascota_personalizada(
    nombre: str = Form(...),
    rareza: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db_session)  # <-- CAMBIADO AQUÍ
):
    # Formatear el nombre para usarlo como nombre de archivo
    nombre_archivo = nombre.lower().replace(" ", "_") + ".png"
    ruta_imagen = f"static/mascotas/{nombre_archivo}"

    # Verificar extensión válida
    ext = os.path.splitext(imagen.filename)[-1].lower()
    if ext not in [".png", ".jpg", ".jpeg"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido")

    # Guardar archivo en disco
    with open(ruta_imagen, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    # Guardar en la base de datos
    mascota_data = {
        "nombre": nombre,
        "rareza": rareza,
        "imagen_url": f"/static/mascotas/{nombre_archivo}",
        "lat": lat,
        "lon": lon
    }

    return agregar_mascota_personalizada(mascota_data, db)