import factory
from django.test import TestCase, Client
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import os
import glob

THE_FILE = SimpleUploadedFile('test.png', 'a photo')
PASSWORD = 'test_password'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'john'
    first_name = 'john'
    last_name = 'doe'
    email = 'john@doe.com'
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    user = UserFactory()
    image = factory.django.ImageField(color='blue')
    file_size = 1000000
    published = 'pvt'


class PhotoTestCase(TestCase):

    def setUp(self):
        UserFactory()

    def tearDown(self):
        for file in glob.glob("media/imager_images/test*.png"):
            os.remove(file)

    def test_photo_has_user(self):
        user_john = User.objects.get(username='john')
        photo1 = Photo()
        photo1.user = user_john
        photo1.image = THE_FILE
        photo1.save()
        self.assertEquals(Photo.objects.all()[0].user, user_john)

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


class LibraryTestCase(TestCase):
    def setup(self):
        self.client = Client()

        self.user1 = UserFactory(username='johndoe')

        self.user1.profile.save()
        self.user1.profile.picture_privacy = True
        self.user1.profile.phone_number = '+12066819318'
        self.user1.profile.phone_privacy = True
        self.user1.profile.birthday = '1999-01-01'
        self.user1.profile.birthday_privacy = True
        self.user1.profile.email_privacy = True
        self.user1.profile.name_privacy = True

        photo1 = PhotoFactory()
        photo2 = PhotoFactory()
        photo3 = PhotoFactory()

        photo1.image = factory.django.ImageField(filename='example1.jpg',
                                                 color='blue')
        photo1.user = self.user1

        photo2.image = factory.django.ImageField(filename='example2.jpg',
                                                 color='blue')
        photo2.user = self.user1

        photo3.image = factory.django.ImageField(filename='example3.jpg',
                                                 color='blue')
        photo3.user = self.user1

        photo1.image.save()
        photo2.image.save()
        photo3.image.save()

        album1 = Album(title='album1')
        album1.user = self.user1
        album2 = Album(title='album2')
        album2.user = self.user1
        album3 = Album(title='album3')
        album3.user = self.user1

        album1.save()
        album2.save()
        album3.save()

        photo1.albums.add(album1)
        photo2.albums.add(album2)
        photo2.albums.add(album2)

        album1.cover = photo1
        album2.cover = photo2

    def tearDown(self):
        for file in glob.glob("media/imager_images/example*.jpg"):
            os.remove(file)

    def test_cover_thumbnails(self):
        import ipdb; ipdb.set_trace()
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/library/')
        print(response.content)
        # self.assertIn(
        #     '<li id="username">Username: {}<span class="privacy"></span></li>'
        #     .format(self.user1.username), response.content)
