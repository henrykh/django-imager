from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import Photo
# from views import AlbumCreate


@receiver(pre_save, sender=Photo)
def set_file_size(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance:
        instance.file_size = instance.image.size

# @receiver(pre_save, sender=AlbumCreate)
# def set_user(sender, **kwargs):
#     import pdb; pdb.set_trace()
#     instance = kwargs.get('instance').user
#     if instance:
#         pass