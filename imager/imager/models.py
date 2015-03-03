from django.db import models
from django.conf import settings


class ImagerProfile(models.Manager):
    def active():
        from django.db import connection
        cursor = connection.cursor()


class profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    objects = ImagerProfile()

    picture = models.FileField()
    picture_privacy = models.BooleanField()

    phone_number = models.CharField()
    phone_privacy = models.BooleanField()

    birthday = models.DateField()
    birthday_privacy = models.BooleanField()

    name_privacy = models.BooleanField()
    email_privacy = models.BooleanField()

    def user(self):
        return self.user.username

    def is_active(self):
        return self.user.is_active
