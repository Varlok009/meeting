from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_path = '/auth/signup/'
        self.login_path = '/auth/login/'
        self.username = 'user_test'
        self.email = 'test@example.com'
        self.password = '12345678!LlDl24'

    def test_signup(self):
        response = self.client.post(
            self.signup_path,
            {
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
            }
        )
        self.assertRedirects(
            response,
            expected_url=self.login_path,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

    def test_login(self):
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        response = self.client.post(self.login_path, {'username': self.username, 'password': self.password})
        self.assertRedirects(
            response,
            expected_url='/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

    def test_user(self):
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        response = self.client.get(f'/{self.username}/')
        self.assertEqual(response.status_code, 200)



