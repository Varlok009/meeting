from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="tv", email="testvarlok@example.com", password="12345"
        )

    def test_user(self):
        self.user = User.objects.get(username='tv')
        self.assertEqual(self.user.username, 'tv', msg='user tv was not created')
        self.assertEqual(self.user.email, 'testvarlok@example.com', msg='user tv has invalid email')

    def test_user_profile(self):
        response = self.client.get('/tv/')
        self.assertEqual(response.status_code, 200, msg='user tv profile was not to created')


