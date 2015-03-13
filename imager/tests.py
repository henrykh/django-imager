from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test_username'
        self.email = 'test@test.com'
        self.password = 'test_password'
        self.test_user = User.objects.create_user('test_username',
                                                  'test@test.com',
                                                  'test_password')
        self.client.post('/accounts/login/',
                         {'username': self.username,
                          'password': self.password})

    def test_loggedin_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='home.html')
        print(response.content)
        self.assertIn('<title>Profile: test_username</title>',
                      response.content)

    def test_loggedin_profile(self):
        response = self.client.get('/profile/')
        self.assertTemplateUsed(response, template_name='profile.html')
        self.assertIn('<title>Profile: test_username</title>',
                      response.content)

