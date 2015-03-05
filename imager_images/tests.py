import factory
from django.test import TestCase
from models import Album, Photo
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = 'john'


class AlbumTestCase(TestCase):
        def setUp(self):
            the_image = factory.django.ImageField(color='blue')

        def test_album(self):
            self.john = UserFactory()
            the_image = factory.django.ImageField(color='blue')
            photo1 = Photo()
            album1 = Album()
            album1.user = self.john
            photo1.album(album1)
            self.assertEqual(photo1.albums_set, album1)
