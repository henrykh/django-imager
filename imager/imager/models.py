from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete


class ImagerProfile(models.Model):

    user = models.OneToOneField(User)

    picture = models.FileField(blank=True)
    picture_privacy = models.BooleanField(default=True)

    phone_number = models.CharField(max_length=20, blank=True)
    phone_privacy = models.BooleanField(default=True)

    birthday = models.DateField(null=True, blank=True)
    birthday_privacy = models.BooleanField(default=True)

    name_privacy = models.BooleanField(default=True)
    email_privacy = models.BooleanField(default=True)

    def user(self):
        return self.associated_user.username

    def is_active(self):
        return self.associated_user.is_active

    @classmethod
    def active(self):
        qs = self.get_queryset()
        return qs.filter(user__is_active=True)


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        ip = ImagerProfile(user=kwargs["instance"])
        ip.save()


def delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()

post_save.connect(create_profile, sender=User)

pre_delete.connect(delete_user, sender=ImagerProfile)
