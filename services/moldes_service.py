from services.firebase import db

def obtener_moldes_mascotas():
    coleccion = db.collection("plantillas_mascotas")
    docs = coleccion.stream()
    moldes = []
    for doc in docs:
        data = doc.to_dict()
        moldes.append({
            "nombre": data["nombre"],
            "rareza": data["rareza"],
            "imagen_url": data["imagen_url"]
        })
    return moldes
