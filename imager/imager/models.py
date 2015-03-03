from django.db import models
from django.contrib.auth.models import User


class ImagerProfile(models.Model):
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
        return self.associated_user.username

    def is_active(self):
        return self.associated_user.is_active

    @classmethod
    def active(self):
        qs = self.get_queryset()
        return qs.filter(associated_user__is_active=True)
