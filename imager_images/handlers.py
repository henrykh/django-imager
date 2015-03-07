from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import Photo


@receiver(pre_save, sender=Photo)
def set_file_size(sender, instance, *args, **kwargs):
    instance.file_size = instance.image.size
