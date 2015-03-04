from django.apps import AppConfig

class ImagerConfig(AppConfig):
    name = 'imager_user'
    verbose_name = "Imager_User"

    def ready(self):
        import handlers
