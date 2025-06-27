import json
import firebase_admin
from firebase_admin import credentials, firestore

# Ruta al archivo de credenciales de Firebase
RUTA_CREDENCIALES = "database/firebase/firebase_config.json"

# Inicializar Firebase
cred = credentials.Certificate(RUTA_CREDENCIALES)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Cargar moldes desde JSON
with open("database/firebase/plantillas_mascotas.json", "r", encoding="utf-8") as f:
    moldes = json.load(f)

# Subir cada molde a la colección "plantillas_mascotas"
for molde in moldes:
    nombre_doc = molde["nombre"].lower().replace(" ", "_")
    db.collection("plantillas_mascotas").document(nombre_doc).set(molde)

print("Plantillas de mascotas subidas correctamente a Firebase Firestore.")
