from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveProfileManager, self).get_queryset()
        return qs.filter(associated_user__is_active__exact=True)


class ImagerProfile(models.Model):

    associated_user = models.OneToOneField(User)

    picture = models.FileField(blank=True)
    picture_privacy = models.BooleanField(default=True)

    phone_number = models.CharField(max_length=20, blank=True)
    phone_privacy = models.BooleanField(default=True)

    birthday = models.DateField(null=True, blank=True)
    birthday_privacy = models.BooleanField(default=True)

    name_privacy = models.BooleanField(default=True)
    email_privacy = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveProfileManager()

    def user(self):
        return self.associated_user

    def is_active(self):
        return self.associated_user.is_active


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        ip = ImagerProfile(associated_user=kwargs["instance"])
        ip.save()

post_save.connect(create_profile, sender=User)

# def delete_user(sender, instance, *args, **kwargs):
#     if instance.associated_user:
#         instance.associated_user.delete()

# pre_delete.connect(delete_user, sender=ImagerProfile)
