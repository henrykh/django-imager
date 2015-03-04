from django.test import TestCase
from models import ImagerProfile
from django.contrib.auth.models import User


class ImagerProfileTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')
        user2.is_active = False
        ImagerProfile(user=user1, phone_number='1')
        ImagerProfile(user=user2, phone_number='2')

    def test_profile_linked_to_user(self):
        user1 = User.objects.get(username='user1')
        profile1 = ImagerProfile.objects.all().filter(phone_number='1')
        self.assertEqual(profile1[0].user, user1)

    def test_user_is_active(self):
        profile1 = ImagerProfile.objects.filter(phone_number='1').all()
        self.assertEqual(profile1[0].is_active(), True)

    def test_user_is_inactive(self):
        profile2 = ImagerProfile.objects.filter(phone_number='2').all()
        self.assertEqual(profile2[0].is_active(), True)


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
