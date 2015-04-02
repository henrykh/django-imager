from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveProfileManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


class ImagerProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    follows = models.ManyToManyField("self",
                                     symmetrical=False,
                                     related_name='followers',
                                     blank=True)
    blocking = models.ManyToManyField("self",
                                      symmetrical=False,
                                      related_name='blocked',
                                      blank=True)

    picture = models.ImageField(upload_to='imager_user', blank=True)
    picture_privacy = models.BooleanField(default=True)

    phone_error = "Number must be in the format: '+999999999'. Up to 15 digits"
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=phone_error)
    phone_number = models.CharField(max_length=32,
                                    validators=[phone_regex],
                                    blank=True)
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
        return self.follows.add(other)

    def unfollow(self, other):
        return self.follows.remove(other)

    def following(self):
        return self.follows.exclude(blocking=self)

    def block(self, other):
        return self.blocking.add(other)

    def unblock(self, other):
        return self.blocking.remove(other)
