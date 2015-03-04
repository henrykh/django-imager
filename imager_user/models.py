from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveProfileManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


class ImagerProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    following = models.ManyToManyField("self", symmetrical=False, related_name='followers')


    picture = models.ImageField(upload_to='imager_user', blank=True)
    picture_privacy = models.BooleanField(default=True)

    phone_number = PhoneNumberField(blank=True)
    phone_privacy = models.BooleanField(default=True)

    birthday = models.DateField(null=True, blank=True)
    birthday_privacy = models.BooleanField(default=True)

    name_privacy = models.BooleanField(default=True)
    email_privacy = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveProfileManager()

    def is_active(self):
        return self.user.is_active

    def __str__(self):
        return self.user.username

    def follow(self, other):
        return self.following.add(other)

    def unfollow(self, other):
        return self.following.remove(other)
