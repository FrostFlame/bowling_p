from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from django.urls import reverse
from django_webtest.pytest_plugin import django_app_factory
from selenium.webdriver.android.webdriver import WebDriver

from accounts.models import User, PlayerInfo, City

csrf_client = Client(enforce_csrf_checks=False)


class AccountsPagesTest(TestCase):
    def test_login_page(self):
        response = self.client.get('/account/login/')
        self.assertEquals(response.status_code, 200)

    def test_registration_page(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get('/account/logout')
        self.assertEquals(response.status_code, 301)

    def test_profile_page(self):
        response = self.client.get('/account/profile/')
        self.assertEquals(response.status_code, 302)

    def test_profile_edit_page(self):
        response = self.client.get('/account/profile/edit')
        self.assertEquals(response.status_code, 302)


class AccountsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(email='alexpetr@m.ru', password='alexpetr@m.ru')
        cls.user.email_confirmed = True
        cls.user.save()

    def setUp(self):
        pass

    def test_login(self):
        response = self.client.post('/account/login/', {
            'username': 'alexpetr@m.ru',
            'password': 'alexpetr@m.ru',
        })
        print(response.content_params.get())
        self.assertEquals(response, 'alexpetr@m.ru')

    def test_logout(self):
        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
