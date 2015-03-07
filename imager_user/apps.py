from django.apps import AppConfig


class ImagerConfig(AppConfig):
    name = 'imager_user'
    verbose_name = "Imager User"

    def ready(self):
        import imager_user.handlers
