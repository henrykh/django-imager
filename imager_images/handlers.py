from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Photo


@receiver(post_save, sender=Photo)
def set_file_size(sender, instance, *args, **kwargs):
    import pdb; pdb.set_trace()
    # if kwargs["created"]:
