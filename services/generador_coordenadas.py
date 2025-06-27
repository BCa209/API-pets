import math
import random

def generar_coordenada_dentro_de_radio(centro, radio_km):
    lat_c, lon_c = centro

    # Radio de la Tierra en km
    R = 6371

    # Conversión de radio a distancia angular
    radio_angular = radio_km / R

    # Ángulo aleatorio
    theta = random.uniform(0, 2 * math.pi)

    # Distancia aleatoria dentro del círculo
    distancia = random.uniform(0, radio_angular)

    delta_lat = distancia * math.cos(theta)
    delta_lon = distancia * math.sin(theta) / math.cos(math.radians(lat_c))

    nueva_lat = lat_c + math.degrees(delta_lat)
    nueva_lon = lon_c + math.degrees(delta_lon)

    return nueva_lat, nueva_lon
