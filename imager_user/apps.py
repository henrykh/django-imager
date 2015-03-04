from django.apps import AppConfig


class ImagerConfig(AppConfig):
    name = 'imager_user'
    verbose_name = "Imager User"

    def ready(self):
        from handlers import create_profile
