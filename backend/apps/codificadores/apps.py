from django.apps import AppConfig


class CodificadoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.codificadores'

    def ready(self):
        from . import signals
