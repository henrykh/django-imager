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

        photo1 = PhotoFactory()
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

        photo1.albums.add(album1)
        photo2.albums.add(album2)

        photo2.albums.add(album3)
        photo3.albums.add(album3)

        thumb1 = get_thumbnail(photo1.image, '1000x1000')
        thumb2 = get_thumbnail(photo2.image, '1000x1000')
        thumb3 = get_thumbnail(photo3.image, '1000x1000')
        thumb4 = get_thumbnail(photo4.image, '1000x1000')
        thumb5 = get_thumbnail(photo5.image, '1000x1000')

        self.thumb_user1_all = [thumb1.url, thumb2.url,
                                thumb3.url, thumb4.url,
                                thumb5.url]
        self.thumb_user1_loose = [thumb4.url, thumb5.url]
        self.thumb_user1_no_cover_album = [thumb2.url, thumb3.url]

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
        self.assertIn(
            '<a href="/media/imager_images/img/man.png" data-lightbox="albumcovers" data-title="{}">'
            .format(self.user1.albums.filter(
                title='album4')[0].description), response.content)

    def test_album_cover_thumbnails_album_no_cover(self):
        response = self.client.get('/library/')
        album_photos = []

        for item in self.thumb_user1_no_cover_album:
            album_photos.append('<a href="{}" data-lightbox="albumcovers" data-title="{}">'
                                .format(item,
                                        self.user1.albums.filter(
                                            title='album3')[0].description))

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


class StreamTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = UserFactory(username='johndoe')
        self.user2 = UserFactory(username='janedoe')
        self.user3 = UserFactory(username='samdoe')

        self.user1.profile.follow(self.user2.profile)

        photo1 = PhotoFactory(published='pub')
        photo1.user = self.user1
        photo1.save()

        photo2 = PhotoFactory(published='pub')
        photo2.user = self.user2
        photo2.save()

        photo3 = PhotoFactory(published='shd')
        photo3.user = self.user2
        photo3.save()

        photo4 = PhotoFactory()
        photo4.user = self.user2
        photo4.save()

        photo5 = PhotoFactory(published='pub')
        photo5.user = self.user3
        photo5.save()

        photo6 = PhotoFactory(published='shd')
        photo6.user = self.user3
        photo6.save()

        thumb1 = get_thumbnail(photo1.image, '1000x1000')
        thumb2 = get_thumbnail(photo2.image, '1000x1000')
        thumb3 = get_thumbnail(photo3.image, '1000x1000')
        thumb4 = get_thumbnail(photo4.image, '1000x1000')
        thumb5 = get_thumbnail(photo5.image, '1000x1000')
        thumb6 = get_thumbnail(photo5.image, '1000x1000')

        self.thumb_user1 = [thumb1.url]
        self.thumb_user2_pub_shd = [thumb2.url, thumb3.url]
        self.thumb_user2_pvt = [thumb4.url]
        self.thumb_user3 = [thumb5.url, thumb6.url]

        self.client.login(username=self.user1.username, password=PASSWORD)

    def tearDown(self):
        for file in glob.glob("media/imager_images/test*"):
            os.remove(file)

    def test_user_photo(self):
        response = self.client.get('/stream/')

        for item in self.thumb_user1:
            self.assertIn('<img src="{}"></a>'.format(item), response.content)

    def test_followed_user_photos_pub_shd(self):
        response = self.client.get('/stream/')

        for item in self.thumb_user2_pub_shd:
            self.assertIn('<img src="{}"></a>'.format(item), response.content)

    def test_followed_user_photos_pvt(self):
        response = self.client.get('/stream/')

        for item in self.thumb_user2_pvt:
            self.assertNotIn('<img src="{}"></a>'.format(item), response.content)

    def test_unfollowed_user_photos(self):
        response = self.client.get('/stream/')

        for item in self.thumb_user3:
            self.assertNotIn('<img src="{}"></a>'.format(item), response.content)

    def test_order_of_stream(self):
        response = self.client.get('/stream/')
        thumbs = self.thumb_user1 + self.thumb_user2_pub_shd

        for i in xrange(len(thumbs)-1):
            self.assertLess(response.content.index(thumbs[i]),
                            response.content.index(thumbs[i+1]))

    def test_owner_photo_credit(self):
        response = self.client.get('/stream/')
        owner = [self.user1.username,
                 self.user2.username,
                 self.user2.username]
        thumbs = self.thumb_user1 + self.thumb_user2_pub_shd

        start = response.content.index('photoStream')
        for i in xrange(len(thumbs)-1):
            a = response.content.index(thumbs[i], start)
            b = response.content.index(owner[i], start)
            self.assertLess(a, b)
            start = b + len(owner[i])


class PhotoUpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = UserFactory(username='johndoe')
        self.user2 = UserFactory(username='janedoe')

        photo1 = PhotoFactory()
        photo1.user = self.user1
        photo1.title = 'Old Title'
        photo1.description = 'Old Description'
        photo1.date_published = '2015-03-17'
        photo1.save()

        album1 = Album(title='album1')
        album1.user = self.user1
        album1.save()

        album2 = Album(title='album2')
        album2.user = self.user1
        album2.save()

        album3 = Album(title='album3')
        album3.user = self.user2
        album3.save()

        photo1.albums.add(album1)

        self.client.login(username=self.user1.username, password=PASSWORD)

    def tearDown(self):
        for file in glob.glob("media/imager_images/test*"):
            os.remove(file)

    def test_intial_values_user_albums_not_selected(self):
        photo_id = self.user1.photos.all()[0].id

        album_id = self.user1.albums.filter(title='album2').all()[0].id
        album_title = self.user1.albums.filter(title='album2').all()[0].title

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertIn(
            '<option value="{}">{}</option>'
            .format(album_id, album_title), response.content)

    def test_intial_values_user_albums_selected(self):
        photo_id = self.user1.photos.all()[0].id

        album_id = self.user1.albums.filter(title='album1').all()[0].id
        album_title = self.user1.albums.filter(title='album1').all()[0].title

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertIn(
            '<option value="{}" selected="selected">{}</option>'
            .format(album_id, album_title), response.content)

    def test_intial_values_non_user_albums_not_choice(self):
        photo_id = self.user1.photos.all()[0].id

        album_id = Album.objects.get(title='album3').id
        album_title = Album.objects.get(title='album3').title

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertNotIn(
            '<option value="{}">{}</option>'
            .format(album_id, album_title), response.content)

    def test_intial_values_photo_title(self):
        photo_id = self.user1.photos.all()[0].id
        photo_title = self.user1.photos.all()[0].title

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertIn(
            '<input id="id_title" maxlength="127" name="title" type="text" value="{}" />'
            .format(photo_title), response.content)

    def test_intial_values_photo_description(self):
        photo_id = self.user1.photos.all()[0].id
        photo_description = self.user1.photos.all()[0].description

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertIn(
            '<textarea cols="40" id="id_description" name="description" rows="10">\r\n{}</textarea></p>'
            .format(photo_description), response.content)

    def test_intial_values_photo_date_published(self):
        photo_id = self.user1.photos.all()[0].id
        photo_date_published = self.user1.photos.all()[0].date_published

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertIn(
            '<input id="id_date_published" name="date_published" type="text" value="{}" /></p>'
            .format(photo_date_published), response.content)

    def test_intial_values_photo_published_choices(self):
        photo_id = self.user1.photos.all()[0].id

        response = self.client.get('/photo/update/{}/'.format(photo_id))

        self.assertIn(
            '<option value="pvt" selected="selected">Private</option>',
            response.content)
        self.assertIn(
            '<option value="shd">Shared</option>',
            response.content)
        self.assertIn(
            '<option value="pub">Public</option>',
            response.content)


class AlbumUpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = UserFactory(username='johndoe')
        self.user2 = UserFactory(username='janedoe')

        photo1 = PhotoFactory()
        photo1.user = self.user1
        photo1.title = 'photo1'
        photo1.save()

        photo2 = PhotoFactory()
        photo2.user = self.user1
        photo2.title = 'photo2'
        photo2.save()

        photo3 = PhotoFactory()
        photo3.user = self.user1
        photo3.title = 'photo3'
        photo3.save()

        photo4 = PhotoFactory()
        photo4.user = self.user2
        photo4.title = 'photo4'
        photo4.save()

        album1 = Album(title='Old Title')
        album1.description = 'Old Description'
        album1.cover = photo1
        album1.date_published = '2015-03-17'
        album1.user = self.user1
        album1.save()

        photo1.albums.add(album1)
        photo2.albums.add(album1)

        self.client.login(username=self.user1.username, password=PASSWORD)

    def tearDown(self):
        for file in glob.glob("media/imager_images/test*"):
            os.remove(file)

    def test_intial_values_album_cover_choice_not_selected(self):
        album_id = self.user1.albums.all()[0].id

        photo_id = self.user1.photos.filter(title='photo2').all()[0].id
        photo_title = self.user1.photos.filter(title='photo2').all()[0].title

        response = self.client.get('/album/update/{}/'.format(album_id))

        end = response.content.index('Published:')
        self.assertTrue(response.content.index(
                        '<option value="{}">{}</option>'
                        .format(photo_id, photo_title), 0, end))

    def test_intial_values_album_cover_choice_selected(self):
        album_id = self.user1.albums.all()[0].id

        photo_id = self.user1.photos.filter(title='photo1').all()[0].id
        photo_title = self.user1.photos.filter(title='photo1').all()[0].title

        response = self.client.get('/album/update/{}/'.format(album_id))

        end = response.content.index('Published:')
        self.assertTrue(response.content.index(
                        '<option value="{}" selected="selected">{}</option>'
                        .format(photo_id, photo_title), 0, end))

    def test_intial_values_album_cover_non_album_photo_not_choice(self):
        album_id = self.user1.albums.all()[0].id

        photo_id = self.user1.photos.filter(title='photo3').all()[0].id
        photo_title = self.user1.photos.filter(title='photo3').all()[0].title

        response = self.client.get('/album/update/{}/'.format(album_id))
        end = response.content.index('Published:')
        with self.assertRaises(ValueError):
            response.content.index(
                '<option value="{}">{}</option>'
                .format(photo_id, photo_title), 0, end)

    def test_intial_values_album_cover_non_user_photo_not_choice(self):
        album_id = self.user1.albums.all()[0].id

        photo_id = Photo.objects.get(title='photo4').id
        photo_title = Photo.objects.get(title='photo4').title

        response = self.client.get('/album/update/{}/'.format(album_id))
        end = response.content.index('Published:')
        with self.assertRaises(ValueError):
            response.content.index(
                '<option value="{}">{}</option>'
                .format(photo_id, photo_title), 0, end)

    def test_intial_values_album_title(self):
        album_id = self.user1.albums.all()[0].id
        album_title = self.user1.albums.all()[0].title

        response = self.client.get('/album/update/{}/'.format(album_id))

        self.assertIn(
            '<input id="id_title" maxlength="127" name="title" type="text" value="{}" />'
            .format(album_title), response.content)

    def test_intial_values_album_description(self):
        album_id = self.user1.albums.all()[0].id
        album_description = self.user1.albums.all()[0].description

        response = self.client.get('/album/update/{}/'.format(album_id))

        self.assertIn(
            '<textarea cols="40" id="id_description" name="description" rows="10">\r\n{}</textarea></p>'
            .format(album_description), response.content)

    def test_intial_values_album_date_published(self):
        album_id = self.user1.albums.all()[0].id
        album_date_published = self.user1.albums.all()[0].date_published

        response = self.client.get('/album/update/{}/'.format(album_id))

        self.assertIn(
            '<input id="id_date_published" name="date_published" type="text" value="{}" /></p>'
            .format(album_date_published), response.content)

    def test_intial_values_album_published_choices(self):
        album_id = self.user1.albums.all()[0].id

        response = self.client.get('/album/update/{}/'.format(album_id))

        self.assertIn(
            '<option value="pvt" selected="selected">Private</option>',
            response.content)
        self.assertIn(
            '<option value="shd">Shared</option>',
            response.content)
        self.assertIn(
            '<option value="pub">Public</option>',
            response.content)

    def test_intial_values_album_photos_not_in_album_choices(self):
        album_id = self.user1.albums.all()[0].id

        response = self.client.get('/album/update/{}/'.format(album_id))

        beg = response.content.index('Published:')

        photo3_id = self.user1.photos.filter(title='photo3').all()[0].id
        photo3_title = self.user1.photos.filter(title='photo3').all()[0].title

        self.assertTrue(response.content.index(
                        '<option value="{}">{}</option>'
                        .format(photo3_id, photo3_title), beg))

    def test_intial_values_album_photo_in_album_not_choice(self):
        album_id = self.user1.albums.all()[0].id

        photo1_id = self.user1.photos.filter(title='photo1').all()[0].id
        photo1_title = self.user1.photos.filter(title='photo1').all()[0].title

        photo2_id = self.user1.photos.filter(title='photo2').all()[0].id
        photo2_title = self.user1.photos.filter(title='photo2').all()[0].title

        response = self.client.get('/album/update/{}/'.format(album_id))
        beg = response.content.index('Published:')

        with self.assertRaises(ValueError):
            response.content.index(
                '<option value="{}">{}</option>'
                .format(photo1_id, photo1_title), beg)

        with self.assertRaises(ValueError):
            response.content.index(
                '<option value="{}">{}</option>'
                .format(photo2_id, photo2_title), beg)
