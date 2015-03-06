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


class UserPhotosManager(models.Manager):
    def get_queryset(self):
        qs = super(UserPhotosManager, self).get_queryset()
        return qs.filter(user__photos=True)


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

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.image)

    image_thumb.allow_tags = True


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

    cover = models.ForeignKey('Photo', null=True, blank=True)

    objects = models.Manager()
    userPhotos = UserPhotosManager()

    def __str__(self):
        return self.title

    def album_photos(self):
        self.photos.all()
