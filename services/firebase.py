# services/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore

# Ruta corregida al archivo de credenciales
cred = credentials.Certificate("database/firebase/firebase_config.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
