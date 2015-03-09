import factory
from django.test import TestCase
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile

THE_FILE = SimpleUploadedFile('test.png', 'a photo')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = 'john'


class PhotoTestCase(TestCase):

    def setUp(self):
        UserFactory()

    def test_photo_has_user(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        photo1.save()
        self.assertEquals(Photo.objects.all()[0].user, user_john) 


class AlbumTestCase(TestCase):
    def setUp(self):
        UserFactory()

    def test_photo_in_album(self):
        photo1 = Photo()
        photo1.user = User.objects.get(username='john')
        photo1.image = THE_FILE
        album1 = Album()
        album1.user = User.objects.get(username='john')
        album1.save()
        photo1.save()
        photo1.albums.add(album1)
        self.assertIn(photo1, album1.photos.all())
