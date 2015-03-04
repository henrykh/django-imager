from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from imager_user.models import ImagerProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        ip = ImagerProfile(user=kwargs["instance"])
        ip.save()
