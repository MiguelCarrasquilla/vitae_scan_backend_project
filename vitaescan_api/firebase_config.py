import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

# Cargamos el archivo JSON con las credenciales del proyecto FIREBASE
if not firebase_admin._apps:
    cred =  credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
    print("Conexión con firebase exitosa")
else:
    print("Firebase ya estaba inicializado")