# services/mascota_generador.py

from models.mascota import Mascota
import random

def generar_mascotas(ubicacion: str, tipo: str, cantidad: int = 5) -> list[Mascota]:
    # Aquí pones tu lógica actual
    mascotas = []
    for i in range(cantidad):
        mascotas.append(Mascota(
            nombre=f"Mascota {i+1}",
            rareza=random.choice(["común", "rara", "legendaria"]),
            ubicacion=ubicacion,
            latitud=random.uniform(-90, 90),
            longitud=random.uniform(-180, 180),
            imagen="https://ejemplo.com/imagen.png"
        ))
    return mascotas
