from django.apps import AppConfig


class ImagerImagesConfig(AppConfig):
    name = 'imager_images'
    verbose_name = "Imager Images"

    def ready(self):
        import imager_images.handlers
