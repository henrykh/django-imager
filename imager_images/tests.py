import factory
from django.test import TestCase
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = 'john'


class AlbumTestCase(TestCase):
        def setUp(self):
            UserFactory()
            self.file = SimpleUploadedFile('test.png', 'a photo')

        def test_album_exists(self):
            user_john = User.objects.get(username='john')
            album1 = Album()
            album1.user = user_john
            album1.save()
            self.assertEqual(Album.objects.get(pk=1).user, user_john)

        def test_photo_in_album(self):
            photo1 = Photo()
            photo1.user = User.objects.get(username='john')
            photo1.image = self.file
            album1 = Album()
            album1.user = User.objects.get(username='john')
            album1.save()
            photo1.save()
            photo1.albums.add(album1)
            self.assertIn(photo1, album1.photos.all())
