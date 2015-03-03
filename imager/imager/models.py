from django.db import models
from django.contrib.auth.models import User


class ImagerProfile(models.Manager):
    def active():
        from django.db import connection
        cursor = connection.cursor()


class profile(models.Model):
    # objects = ImagerProfile()

    associated_user = models.OneToOneField(User)

    picture = models.FileField(blank=True)
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
