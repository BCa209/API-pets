###model/mascota_sqlite.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MascotaDB(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String)
    rareza = Column(String)
    imagen_url = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    ubicacion = Column(String)
