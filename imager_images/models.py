from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail

PRIVATE = 'pvt'
SHARED = 'shd'
PUBLIC = 'pub'
PHOTO_PRIVACY_OPTIONS = (
    (PRIVATE, 'Private'),
    (SHARED, 'Shared'),
    (PUBLIC, 'Public'),
)


class UserPhotosManager(models.Manager):
    def get_queryset(self):
        qs = super(UserPhotosManager, self).get_queryset()
        return qs.filter(user__photos=True)


class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    image = ImageField(upload_to='imager_images')
    file_size = models.IntegerField(null=True, blank=True)
    albums = models.ManyToManyField('Album', related_name='photos', blank=True)

    title = models.CharField(max_length=127, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateField(auto_now=True, null=True)
    date_published = models.DateField(null=True, blank=True)

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)

    def image_thumbnail(self):
        if self.image:
            thumb = get_thumbnail(
                self.image, "50x50", crop='center', quality=99)
            return '<img src="%s"/>' % (thumb.url)
        else:
            return 'No Image'

    def __str__(self):
        return self.title


class Album(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    title = models.CharField(max_length=127, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateField(auto_now=True, null=True)
    date_published = models.DateField(null=True, blank=True)

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)

    cover = models.ForeignKey('Photo', null=True, blank=True)

    objects = models.Manager()
    userPhotos = UserPhotosManager()

    def __str__(self):
        return self.title

    def cover_thumbnail(self,):
        if self.cover:
            thumb = get_thumbnail(
                self.cover, "50x50", crop='center', quality=99)
            return '<img src="%s"/>' % (thumb.url)
        else:
            return 'No Image'

    def album_photos(self):
        self.photos.all()
