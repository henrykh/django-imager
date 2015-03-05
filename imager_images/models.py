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


class Album(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True, blank=True)

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)

    # def create_cover_choices(self):
    #     photo_paths = self.photos.all().image.name
    #     choices = ()
    #     for path in photo_paths:
    #         choices + ((path, path.split('/')[-1]),)
    #     return choices

    # cover = models.CharField(blank=True, choices=create_cover_choices())


class Photo(models.Model):
    image = models.ImageField(upload_to='imager_images', blank=True)
    user = models.ForeignKey(User, related_name='photos')
    albums = models.ManyToManyField(Album, related_name='photos')

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True, blank=True)

    published = models.CharField(max_length=3,
                                 choices=PHOTO_PRIVACY_OPTIONS,
                                 default=PRIVATE)

    def album(self, other):
        return self.albums.add(other)
