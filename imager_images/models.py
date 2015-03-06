from django.db import models
from django.contrib.auth.models import User


PRIVATE = 'pvt'
SHARED = 'shd'
PUBLIC = 'pub'
PHOTO_PRIVACY_OPTIONS = (
    (PRIVATE, 'Private'),
    (SHARED, 'Shared'),
    (PUBLIC, 'Public'),
)


class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    image = models.ImageField(upload_to='imager_images', blank=True)
    albums = models.ManyToManyField('Album', related_name='photos', blank=True)

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateField(auto_now=True, null=True)
    date_published = models.DateField(null=True, blank=True)

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)

    def __str__(self):
        return self.title


class Album(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateField(auto_now=True, null=True)
    date_published = models.DateField(null=True, blank=True)

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)

    cover = models.ForeignKey('Photo', null=True)

    def __str__(self):
        return self.title

    def album_photos(self):
        self.photos.all()
