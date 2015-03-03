from django.db import models
from django.conf import settings


# class ImagerProfile(models.Manager):
#     def active():
#         from django.db import connection
#         cursor = connection.cursor()


class profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # objects = ImagerProfile()

    picture = models.FileField()
    picture_privacy = models.BooleanField(default=True)

    phone_number = models.CharField(max_length=20)
    phone_privacy = models.BooleanField(default=True)

    birthday = models.DateField()
    birthday_privacy = models.BooleanField(default=True)

    name_privacy = models.BooleanField(default=True)
    email_privacy = models.BooleanField(default=True)

    def user(self):
        return self.user.username

    def is_active(self):
        return self.user.is_active
