from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Group


class UserPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tv", email="testvarlok@example.com", password="12345")
        self.client.login(username='tv', password='12345')
        self.new_post_path = '/new'

    def test_create_post(self):
        """Test creation a post from an auth user
        then from an anonim user"""
        response = self.client.get(self.new_post_path)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.new_post_path,
            {'text': 'hello test', 'author': self.user},
            follow=True
        )
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertEqual(len(response.context['page'].object_list), 1)
        self.assertEqual(response.context['page'].object_list[0].text, 'hello test')
        self.assertEqual(response.context['page'].object_list[0].author.username, self.user.username)

        self.client.logout()
        response = self.client.get(self.new_post_path, follow=True)
        self.assertRedirects(
            response,
            f'/auth/login/?next={self.new_post_path}',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
            )

    def test_edit_post(self):
        """
        Test to edit user's post from user
        then edit user's post from anonymous
        and edit user's post from another user
        """
        response = self.client.post(
            self.new_post_path,
            {'text': 'hello test', 'author': self.user},
            follow=True
        )
        self.post_id = response.context['page'].object_list[0].id

        response = self.client.get(f'/{self.user}/{self.post_id}/edit/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            f'/{self.user}/{self.post_id}/edit/',
            {'text': 'hello test edit', 'author': self.user},
            follow=True
        )
        self.assertRedirects(
            response,
            f'/{self.user}/{self.post_id}/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertEqual(response.context['post'].text, 'hello test edit')
        self.assertEqual(response.context['post'].author.username, self.user.username)

        response = self.client.get(f'/{self.user}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'].object_list[0].text, 'hello test edit')
        self.assertEqual(response.context['page'].object_list[0].author.username, self.user.username)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'].object_list[0].text, 'hello test edit')
        self.assertEqual(response.context['page'].object_list[0].author.username, self.user.username)

        self.client.logout()
        self.user2 = User.objects.create_user(username="tv2", email="testvarlok2@example.com", password="12345")
        self.client.login(username='tv2', password='12345')

        response = self.client.get(f'/{self.user}/{self.post_id}/edit/', follow=True)
        self.assertRedirects(
            response,
            f'/{self.user}/{self.post_id}/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
