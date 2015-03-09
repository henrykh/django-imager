import factory
from django.test import TestCase
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import os
import glob

THE_FILE = SimpleUploadedFile('test.png', 'a photo')


def clean_up():
    for file in glob.glob("media/imager_images/test*.png"):
        os.remove(file)


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
        clean_up()

    def test_photo_metadata(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        photo1.title = "Image Title"
        photo1.description = "An Image"
        photo1.published = "pvt"
        photo1.save()
        the_photo = Photo.objects.all()[0]
        self.assertEquals(the_photo.title, "Image Title")
        self.assertEquals(the_photo.description, "An Image")
        self.assertEquals(the_photo.published, "pvt")
        self.assertEquals(the_photo.date_uploaded, datetime.date.today())
        self.assertEquals(the_photo.date_modified, datetime.date.today())
        clean_up()


class AlbumTestCase(TestCase):
    def setUp(self):
        UserFactory()
        UserFactory(username='jane')
        self.file = SimpleUploadedFile('test.png', 'a photo')

    def test_album_owner(self):
        user_john = User.objects.get(username='john')
        album1 = Album()
        album1.user = user_john
        album1.save()
        self.assertEqual(Album.objects.all()[0].user, user_john)
        clean_up()

    def test_photo_in_album(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        album1 = Album()
        album1.user = user_john
        album1.save()
        photo1.save()
        photo1.albums.add(album1)
        self.assertIn(photo1, album1.photos.all())
        clean_up()

    def test_photos_in_album(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        photo2 = Photo()
        photo2.user = user_john
        photo2.image = THE_FILE
        album1 = Album()
        album1.user = user_john
        album1.save()
        photo1.save()
        photo2.save()
        photo1.albums.add(album1)
        photo2.albums.add(album1)
        self.assertIn(photo1, album1.photos.all())
        self.assertIn(photo2, album1.photos.all())
        clean_up()

    def test_photo_in_multiple_albums(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        album1 = Album()
        album1.user = user_john
        album2 = Album()
        album2.user = user_john
        album1.save()
        album2.save()
        photo1.save()
        photo1.albums.add(album1)
        photo1.albums.add(album2)
        self.assertIn(photo1, album1.photos.all())
        self.assertIn(photo1, album2.photos.all())
        clean_up()

    def test_album_metadata(self):
        user_john = User.objects.get(username='john')
        album1 = Album()
        album1.user = user_john
        album1.title = "Album Title"
        album1.description = "An Album"
        album1.published = "pvt"
        album1.save()
        the_album = Album.objects.all()[0]
        self.assertEquals(the_album.title, "Album Title")
        self.assertEquals(the_album.description, "An Album")
        self.assertEquals(the_album.published, "pvt")
        self.assertEquals(the_album.date_uploaded, datetime.date.today())
        self.assertEquals(the_album.date_modified, datetime.date.today())
        clean_up()

    def test_album_cover(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        photo1.save()
        album1 = Album()
        album1.user = user_john
        album1.cover = photo1
        album1.save()
        the_album = Album.objects.all()[0]
        self.assertEquals(the_album.cover, photo1)
        clean_up()
