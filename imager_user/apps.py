from django.apps import AppConfig

class ImagerConfig(AppConfig):
    name = 'imager'
    verbose_name = "Imager"

    def ready(self):
        import handlers
