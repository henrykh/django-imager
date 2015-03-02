from django.db import models


class profile(models.Model):
    picture = models.FileField()
    picture_privacy = models.BooleanField()

    phone_number = models.CharField()
    phone_privacy = models.BooleanField()

    birthday = models.DateField()
    birthday_privacy = models.BooleanField()

    name_privacy = models.BooleanField()
    email_privacy = models.BooleanField()

    def profile_user():
        pass

    def is_active():
        pass
