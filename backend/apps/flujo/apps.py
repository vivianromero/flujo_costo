from django.apps import AppConfig

class FlujoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.flujo'

    def ready(self):
        from . import signals




