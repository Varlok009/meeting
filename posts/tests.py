from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class UserPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tv", email="testvarlok@example.com", password="12345")
        self.client.login(username='tv', password='12345')

    def test_create_post(self):
        """Test creation a post from an auth user
        then from an anonim user"""

        new_post_path = '/new'

        response = self.client.post(new_post_path, {'text': 'hello test', 'author': self.user}, follow=True)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        self.client.logout()
        response = self.client.get(new_post_path, follow=True)
        self.assertRedirects(
            response,
            f'/auth/login/?next={new_post_path}',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
            )
