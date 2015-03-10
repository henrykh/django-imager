from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User


class LoginLogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'agconti'
        self.email = 'test@test.com'
        self.password = 'test'
        self.test_user = User.objects.create_user(self.username,
                                                  self.email,
                                                  self.password)
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertEqual(login, True)

    def test_login(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 't1', 'password': 't1'})
        print(response)
