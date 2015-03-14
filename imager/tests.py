import factory
from django.core import mail
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo
import os

PASSWORD = 'test_password'


# class betterfactoryImageField(factory.django.ImageField):
#     def _make_data(self, params):
#         size = params.get('size', 1000000)
#         return super(betterfactoryImageField, self)._make_data(self, params)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = 'test_username'
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    user = UserFactory()
    image = factory.django.ImageField(color='blue')
    file_size = 1000000
    published = 'pvt'


class LoggedOutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logged_out_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='home.html')
        self.assertIn('Welcome to Imgr! Sign up to share images and be awesome!',
                      response.content)

    def test_logged_out_home_links(self):
        response = self.client.get('/')
        self.assertIn('<a href="/">', response.content)
        self.assertIn('<a href="/accounts/login/">', response.content)
        self.assertIn('<a href="/accounts/register/">', response.content)

    def test_logged_out_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertIn('<a href="/accounts/register/">Register</a>!',
                      response.content)
        self.assertIn('<input type="submit" value="Log in" />',
                      response.content)

    def test_logged_out_registration_page(self):
        response = self.client.get('/accounts/register/')
        self.assertIn('<h1>Register Here</h1>',
                      response.content)

    def test_logged_out_profile(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.items()[3][1],
                         'http://testserver/accounts/login/?next=/profile/')

    def test_logged_out_stream(self):
        response = self.client.get('/stream/')
        self.assertEqual(response.items()[3][1],
                         'http://testserver/accounts/login/?next=/stream/')

    def test_logged_out_library(self):
        response = self.client.get('/library/')
        self.assertEqual(response.items()[3][1],
                         'http://testserver/accounts/login/?next=/library/')


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.username = 'test_username'
        UserFactory(username=self.username)
        self.client.login(username=self.username, password=PASSWORD)

    def test_login_redirect_success(self):
        UserFactory()
        response = self.client.post('/accounts/login/',
                                    {'username': 'test_username',
                                     'password': PASSWORD})
        self.assertRedirects(response, '/')

    def test_login_redirect_failuse(self):
        UserFactory()
        response = self.client.post('/accounts/login/',
                                    {'username': 'wrong',
                                     'password': 'wrong'})
        self.assertIn('Please enter a correct username and password',
                      response.content)

    def test_logged_in_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='home.html')
        self.assertIn('Welcome back {}! Continue being awesome!'.format(self.username),
                      response.content)

    def test_logged_in_home_links(self):
        response = self.client.get('/')
        self.assertIn('<a href="/">', response.content)
        self.assertIn('<a href="/profile/">', response.content)
        self.assertIn('<a href="/stream/">', response.content)
        self.assertIn('<a href="/library/">', response.content)
        self.assertIn('<a href="/accounts/logout/?next=/">', response.content)

    def test_logged_in_home_no_public_photos(self):
        ImageFactory()
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='home.html')
        self.assertIn('imager_images/Space_Needle002.jpg',
                      response.content)

    def test_logged_in_home_public_photos(self):
        ImageFactory(published='pub')
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='home.html')
        self.assertIn('imager_images/example',
                      response.content)
        os.system('rm -r media/imager_images/example*')

    def test_logged_in_profile(self):
        response = self.client.get('/profile/')
        self.assertTemplateUsed(response, template_name='profile.html')
        self.assertIn("{}'s Profile".format(self.username),
                      response.content)

    def test_logged_in_stream(self):
        response = self.client.get('/stream/')
        self.assertTemplateUsed(response, template_name='stream.html')
        self.assertIn("{}'s Stream".format(self.username),
                      response.content)

    def test_logged_in_library(self):
        response = self.client.get('/library/')
        self.assertTemplateUsed(response, template_name='library.html')
        self.assertIn("{}'s Library".format(self.username),
                      response.content)


class RegistrationTest(TestCase):
    def test_registration_success(self):
        response = self.client.post('/accounts/register/', {'username': 'username',
                                                'password1': 'password',
                                                'password2': 'password',
                                                'email': 'user@test.com'})

        self.assertRedirects(response, '/accounts/register/complete/')
        self.assertTrue(User.objects.get(username='username'))

        response = self.client.post('/accounts/login/',
                                    {'username': 'username',
                                     'password': 'password'})

        self.assertIn('This account is inactive.',response.content)
