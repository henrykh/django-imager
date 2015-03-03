from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from imager.models import ImagerProfile


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs["created"]:
        ip = ImagerProfile(associated_user=kwargs["instance"])
        ip.save()
