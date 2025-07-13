###services/db_service.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, Session
from models.mascota_sqlite import Base, MascotaDB
from models.mascota import Mascota, MascotaActualizar

DATABASE_PATH = "database/sqlite/mascotas.sqlite"
DATABASE_URL = f"sqlite:///./{DATABASE_PATH}"

DB_PATH = Path(DATABASE_PATH)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Agrega esto al final de tu archivo
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Inicializar la tabla
def init_db():
    Base.metadata.create_all(bind=engine)

# Guardar una lista de mascotas en la base de datos
def guardar_mascotas_en_db(mascotas: list[MascotaDB]):
    db = SessionLocal()
    for mascota in mascotas:
        db.add(mascota)  # SQLite asigna ID automáticamente
    db.commit()
    db.close()

# Obtener mascotas por ubicación
def obtener_mascotas_por_ubicacion(ubicacion: str) -> list[Mascota]:
    db = SessionLocal()
    try:
        mascotas = db.query(MascotaDB).filter(MascotaDB.ubicacion == ubicacion).all()
        return [
            Mascota(
                id=m.id,
                nombre=m.nombre,
                rareza=m.rareza,
                imagen_url=m.imagen_url,
                lat=m.lat,
                lon=m.lon
            ) for m in mascotas
        ]
    finally:
        db.close()

# Eliminar mascotas por ubicación
def eliminar_mascotas_por_ubicacion(ubicacion: str) -> int:
    db = SessionLocal()
    stmt = delete(MascotaDB).where(MascotaDB.ubicacion == ubicacion)
    result = db.execute(stmt)
    db.commit()
    db.close()
    return result.rowcount

# Actualizar mascota
def actualizar_mascota_en_db(id: int, datos: MascotaActualizar) -> Mascota | None:
    db = SessionLocal()
    mascota = db.query(MascotaDB).filter(MascotaDB.id == id).first()
    if not mascota:
        db.close()
        return None
    mascota.nombre = datos.nombre
    mascota.rareza = datos.rareza
    mascota.imagen_url = datos.imagen_url
    mascota.lat = datos.lat
    mascota.lon = datos.lon
    db.commit()
    db.refresh(mascota)
    db.close()
    return Mascota(
        id=mascota.id,
        nombre=mascota.nombre,
        rareza=mascota.rareza,
        imagen_url=mascota.imagen_url,
        lat=mascota.lat,
        lon=mascota.lon
    )

# Obtener TODAS las mascotas (sin filtrar por ubicación)
def obtener_todas_las_mascotas() -> list[Mascota]:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mascotas")
    rows = cursor.fetchall()
    conn.close()

    return [Mascota(**dict(row)) for row in rows] if rows else []

# db_service.py

def obtener_todas_mascotas() -> list[Mascota]:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mascotas")
    rows = cursor.fetchall()
    return [Mascota(**dict(row)) for row in rows] if rows else []

#eliminar mascotas individualmente por coordenadas
def eliminar_mascota_por_coordenadas(lat: float, lon: float) -> int:
    db = SessionLocal()
    rows_eliminadas = db.query(MascotaDB).filter(MascotaDB.lat == lat, MascotaDB.lon == lon).delete()
    db.commit()
    db.close()
    return rows_eliminadas
