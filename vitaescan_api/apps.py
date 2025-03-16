from django.apps import AppConfig


class VitaescanApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vitaescan_api'

    def ready(self):
        from . import firebase_config
