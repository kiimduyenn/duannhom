from django.apps import AppConfig

class DivaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DIVA'

    def ready(self):
        import DIVA.signals
