import factory
from django.test import TestCase, Client
from django.contrib.auth.models import User
from imager_user.models import ImagerProfile
from imager_images.models import Photo, Album
import os
import glob


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


class ImagerProfileTestCase(TestCase):
    def setUp(self):
        UserFactory()
        UserFactory(username='jane', is_active=False)

    def test_profile_linked_to_user(self):
        self.assertEqual(
            type(User.objects.get(username='john').profile), ImagerProfile)

    def test_user_is_active(self):
        self.assertEqual(
            User.objects.get(username='john').profile.is_active(), True)

    def test_user_is_inactive(self):
        self.assertEqual(
            User.objects.get(username='jane').profile.is_active(), False)


class ActiveProfileManagerTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')
        user2.is_active = False
        user1.save()
        user2.save()

        profile1 = ImagerProfile()
        profile1.user = user1
        profile2 = ImagerProfile()
        profile2.user = user2

    def test_list_is_active_users_true(self):
        user1 = User.objects.get(username='user1')
        profile1 = ImagerProfile.objects.get(user=user1)

        self.assertEqual(ImagerProfile.active.all()[0].user, profile1.user)

    def test_list_is_active_users_false(self):
        user2 = User.objects.get(username='user2')
        profile2 = ImagerProfile.objects.get(user=user2)

        self.assertNotEqual(ImagerProfile.active.all()[0].user, profile2.user)


class FollowingTestCase(TestCase):
    def setUp(self):
        self.john = UserFactory()
        self.jane = UserFactory(username='jane')

    def test_follow(self):
        self.john.profile.follow(self.jane.profile)
        self.assertIn(self.jane.profile, self.john.profile.follows.all())

    def test_followers(self):
        self.john.profile.follow(self.jane.profile)
        self.assertIn(self.john.profile, self.jane.profile.followers.all())

    def test_unfollow(self):
        self.john.profile.follow(self.jane.profile)
        self.john.profile.unfollow(self.jane.profile)
        self.assertNotIn(self.jane.profile, self.john.profile.follows.all())

    def test_block(self):
        self.john.profile.follow(self.jane.profile)
        self.jane.profile.block(self.john.profile)
        self.assertNotIn(self.jane.profile, self.john.profile.following())

    def test_unblock(self):
        self.john.profile.follow(self.jane.profile)
        self.jane.profile.block(self.john.profile)
        self.assertNotIn(self.jane.profile, self.john.profile.following())
        self.jane.profile.unblock(self.john.profile)
        self.assertIn(self.jane.profile, self.john.profile.following())


class ProfilePageTestCase(TestCase):
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
        self.user1.profile.save()

        self.user2.profile.picture_privacy = False
        self.user2.profile.phone_number = '+19712796535'
        self.user2.profile.phone_privacy = False
        self.user2.profile.birthday = '1999-10-31'
        self.user2.profile.birthday_privacy = False
        self.user2.profile.email_privacy = False
        self.user2.profile.name_privacy = False
        self.user2.profile.save()

        self.user1.profile.follow(self.user2.profile)

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

        photo1.image
        photo2.image
        photo3.image

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

        self.user1.profile.picture = photo1.image

    def tearDown(self):
        for file in glob.glob("media/imager_images/example*.jpg"):
            os.remove(file)

    def test_profile_page_links(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<a href="/">', response.content)
        self.assertIn('<a href="/profile/">', response.content)
        self.assertIn('<a href="/stream/">', response.content)
        self.assertIn('<a href="/library/">', response.content)
        self.assertIn('<a href="/accounts/logout/?next=/">', response.content)
        self.assertIn('href="/profile/update/', response.content)

    def test_profile_page_no_profile_image(self):
        self.client.login(username=self.user2.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<img src="/static/imager_user/man.png">',
                      response.content)

    def test_profile_page_profile_image(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<img src="/static/imager_images/example.jpg">',
                      response.content)

    def test_profile_page_no_albums(self):
        self.client.login(username=self.user2.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<li>0 albums,</li>', response.content)

    def test_profile_page_albums(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<li>3 albums,</li>', response.content)

    def test_profile_page_no_photos(self):
        self.client.login(username=self.user2.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<li>You have 0 photos,</li>', response.content)

    def test_profile_page_photos(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<li>You have 3 photos,</li>', response.content)

    def test_profile_page_no_followers(self):
        self.client.login(username=self.user2.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<li>and 1 followers</li>', response.content)

    def test_profile_page_followers(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn('<li>and 0 followers</li>', response.content)

    def test_profile_info_false(self):
        self.client.login(username=self.user2.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn(
            '<li id="username">Username: {}<span class="privacy"></span></li>'
            .format(self.user2.username), response.content)
        self.assertIn(
            '<li id="first_name">First Name: {}<span class="privacy">False</span></li>'
            .format(self.user2.first_name), response.content)
        self.assertIn(
            '<li id="last_name">Last Name: {}<span class="privacy">False</span></li>'
            .format(self.user2.last_name), response.content)
        self.assertIn(
            '<li id="email">Email: {}<span class="privacy">False</span></li>'
            .format(self.user2.email), response.content)
        self.assertIn(
            '<li id="phone_number">Phone: {}<span class="privacy">False</span></li>'
            .format(self.user2.profile.phone_number), response.content)
        self.assertIn(
            '<li id="birthday">Birthday: {}<span class="privacy">False</span></li>'
            .format('Oct. 31, 1999'), response.content)

    def test_profile_info_true(self):
        self.client.login(username=self.user1.username, password=PASSWORD)
        response = self.client.get('/profile/')
        self.assertIn(
            '<li id="username">Username: {}<span class="privacy"></span></li>'
            .format(self.user1.username), response.content)
        self.assertIn(
            '<li id="first_name">First Name: {}<span class="privacy">True</span></li>'
            .format(self.user1.first_name), response.content)
        self.assertIn(
            '<li id="last_name">Last Name: {}<span class="privacy">True</span></li>'
            .format(self.user1.last_name), response.content)
        self.assertIn(
            '<li id="email">Email: {}<span class="privacy">True</span></li>'
            .format(self.user1.email), response.content)
        self.assertIn(
            '<li id="phone_number">Phone: {}<span class="privacy">True</span></li>'
            .format(self.user1.profile.phone_number), response.content)
        self.assertIn(
            '<li id="birthday">Birthday: {}<span class="privacy">True</span></li>'
            .format('Jan. 1, 1999'), response.content)
