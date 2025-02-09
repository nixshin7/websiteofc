from django.apps import AppConfig


class AppofcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appofc'

    def ready(self):
        import appofc.signals  # Import the signals
