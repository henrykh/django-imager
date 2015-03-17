import factory
from django.test import TestCase, Client
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import os
import glob
from sorl.thumbnail import get_thumbnail


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
    image = THE_FILE
    title = factory.Sequence(lambda n: 'test{0}'.format(n))
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
    def setUp(self):
        self.client = Client()

        self.user1 = UserFactory(username='johndoe')
        self.user2 = UserFactory(username='janedoe')

        self.user2.first_name = 'jane'
        self.user2.last_name = 'doe'
        self.user2.email = 'jane@doe.com'
        self.user2.save()

        self.user1.profile.picture_privacy = True
        self.user1.profile.phone_number = '+12066819318'
        self.user1.profile.phone_privacy = True
        self.user1.profile.birthday = '1999-01-01'
        self.user1.profile.birthday_privacy = True
        self.user1.profile.email_privacy = True
        self.user1.profile.name_privacy = True
        self.user1.profile.picture = THE_FILE
        self.user1.profile.save()

        self.user2.profile.picture_privacy = True
        self.user2.profile.phone_number = '+12066819318'
        self.user2.profile.phone_privacy = True
        self.user2.profile.birthday = '1999-01-01'
        self.user2.profile.birthday_privacy = True
        self.user2.profile.email_privacy = True
        self.user2.profile.name_privacy = True
        self.user2.profile.picture = THE_FILE
        self.user2.profile.save()

        self.user1.profile.follow(self.user2.profile)

        photo1 = PhotoFactory(published='pub')
        photo1.user = self.user1
        photo1.save()

        photo2 = PhotoFactory()
        photo2.user = self.user1
        photo2.save()

        photo3 = PhotoFactory()
        photo3.user = self.user1
        photo3.save()

        photo4 = PhotoFactory()
        photo4.user = self.user1
        photo4.save()

        photo5 = PhotoFactory()
        photo5.user = self.user1
        photo5.save()

        photo6 = PhotoFactory(published='pub')
        photo6.user = self.user2
        photo6.save()

        album1 = Album(title='album1')
        album1.user = self.user1
        album1.cover = photo1
        album1.save()

        album2 = Album(title='album2')
        album2.user = self.user1
        album2.cover = photo2
        album2.save()

        album3 = Album(title='album3')
        album3.description = 'album3'
        album3.user = self.user1
        album3.save()

        album4 = Album(title='album4')
        album4.description = 'album4'
        album4.user = self.user1
        album4.save()

        album6 = Album(title='album6')
        album6.user = self.user2
        album6.cover = photo6
        album6.save()

        photo1.albums.add(album1)
        photo2.albums.add(album2)

        photo2.albums.add(album3)
        photo3.albums.add(album3)

        photo6.albums.add(album6)

        thumb1 = get_thumbnail(photo1.image, '1000x1000')
        thumb2 = get_thumbnail(photo2.image, '1000x1000')
        thumb3 = get_thumbnail(photo3.image, '1000x1000')
        thumb4 = get_thumbnail(photo4.image, '1000x1000')
        thumb5 = get_thumbnail(photo5.image, '1000x1000')
        thumb6 = get_thumbnail(photo5.image, '1000x1000')

        self.thumb_user1_all = [thumb1.url, thumb2.url,
                                thumb3.url, thumb4.url,
                                thumb5.url]
        self.thumb_user1_loose = [thumb4.url, thumb5.url]
        self.thumb_user1_no_cover_album = [thumb2.url, thumb3.url]

        self.thumb_user2_all = [thumb6.url]

        self.client.login(username=self.user1.username, password=PASSWORD)

    def tearDown(self):
        for file in glob.glob("media/imager_images/test*"):
            os.remove(file)

    def test_album_cover_thumbnails_all_photos(self):
        response = self.client.get('/library/')
        all_photos = []

        for item in self.thumb_user1_all:
            all_photos.append(
                '<a href="{}" data-lightbox="albumcovers" data-title="All Photos">'
                .format(item))

        for item in all_photos:
            try:
                assert item in response.content
            except AssertionError:
                continue
            else:
                break
        else:
            self.assertTrue(False)

    def test_album_cover_thumbnails_loose_photos(self):
        response = self.client.get('/library/')
        loose_photos = []

        for item in self.thumb_user1_loose:
            loose_photos.append(
                '<a href="{}" data-lightbox="albumcovers" data-title="Loose Photos">'
                .format(item))

        for item in loose_photos:
            try:
                assert item in response.content
            except AssertionError:
                continue
            else:
                break
        else:
            self.assertTrue(False)

    def test_album_cover_thumbnails_album_no_photos(self):
        response = self.client.get('/library/')
        test = '<a href="/media/imager_images/img/man.png" data-lightbox="albumcovers" data-title="{}">'.format(self.user1.albums.filter(title='album4')[0].description)
        self.assertIn(test, response.content)

    def test_album_cover_thumbnails_album_no_cover(self):
        response = self.client.get('/library/')
        album_photos = []
        print(response.content)
        for item in self.thumb_user1_no_cover_album:
            print(item)
            album_photos.append('<a href="{}" data-lightbox="albumcovers" data-title="{}">'
                                .format(item,
                                        self.user1.albums.filter(title='album3')[0].description))

        import ipdb; ipdb.set_trace()
        

        for item in album_photos:
            try:
                assert item in response.content
            except AssertionError:
                continue
            else:
                break
        else:
            self.assertTrue(False)

    def test_album_titles(self):
        response = self.client.get('/library/')
        for item in self.user1.albums.all():
            self.assertIn('{}</a>'
                          .format(item.title), response.content)
        self.assertIn('All Photos</a>'
                      .format(item.id), response.content)
        self.assertIn('Loose Photos</a>'
                      .format(item.title), response.content)

    def test_album_links(self):
        response = self.client.get('/library/')
        for item in self.user1.albums.all():
            self.assertIn('<a href="/album/{}/">'
                          .format(item.id), response.content)
        self.assertIn('<a href="/photos/loose/">'
                      .format(item.id), response.content)
        self.assertIn('<a href="/photos/all/">'
                      .format(item.id), response.content)
