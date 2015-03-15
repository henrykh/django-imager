import factory
from django.test import TestCase
from django.contrib.auth.models import User
from imager_user.models import ImagerProfile
from imager_images.models import Photo, Album


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',
                                'first_name',
                                'last_name',
                                'email',
                                'password')

    username = 'john'
    first_name = 'john',
    last_name = 'doe',
    email = 'john@doe.com',
    password = 'secret'


class ImageFactory(factory.django.DjangoModelFactory):
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

        user1 = {'username': 'johndoe',
                 'first_name': 'john',
                 'last_name': 'doe',
                 'email': 'john@doe.com',
                 'password': 'secret'}

        profile1 = {'user': 'self.u1',
                    'picture_privacy': 'False',
                    'phone_number': '+12066819318',
                    'phone_privacy': 'True',
                    'birthday': '1999-01-01',
                    'birthday_privacy': 'True',
                    'email_privacy': 'True',
                    'name_privacy': 'False'}

        user2 = {'username': 'janedoe',
                 'first_name': 'jane',
                 'last_name': 'doe',
                 'email': 'jane@doe.com',
                 'password': 'secret'}

        profile2 = {'user': 'self.u2'
                    'picture_privacy': 'False',
                    'phone_number': '+19712796535',
                    'phone_privacy': 'True',
                    'birthday': '1999-10-31',
                    'birthday_privacy': 'True',
                    'email_privacy': 'True',
                    'name_privacy': 'False'}

        self.u1 = UserFactory(username=user1['username'])
        self.u2 = UserFactory(username=user2['username'])
        self.p1 = ImagerProfile()
        self.p2 = ImagerProfile()

        for key in user1:
            self.u1.key = user1[key]
            self.u2.key = user1[key]

        for key in profile1:
            self.p1.key = profile1[key]
            self.p2.key = profile2[key]

        self.u1.profile.follow(self.u2.profile)

        self.image1 = ImageFactory(filename='example1.jpg')
        self.image2 = ImageFactory(filename='example2.jpg')
        self.image3 = ImageFactory(filename='example3.jpg')

        self.image1.user = self.u1
        self.image2.user = self.u2
        self.image3.user = self.u3

        self.album1 = Album()
        self.album2 = Album()
        self.album3 = Album()

    def test_setup(self):
        # import ipdb; ipdb.set_trace()

        for item in self.u1:
            print(item)
