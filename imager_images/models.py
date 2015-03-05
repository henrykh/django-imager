from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    pass


class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    albums = models.ManyToManyField(Album, related_name='photos')

    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(null=True, blank=True)
    date_modified = models.DateField(null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)

    PRIVATE = 'pvt'
    SHARED = 'shd'
    PUBLIC = 'pub'
    PHOTO_PRIVACY_OPTIONS = (
        (PRIVATE, 'Private'),
        (SHARED, 'Shared'),
        (PUBLIC, 'Public'),
    )

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)
