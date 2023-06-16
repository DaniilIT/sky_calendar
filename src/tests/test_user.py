from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import User


class UserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='Pq9#tDF1')
        self.user = User.objects.create_user(username='test_user', password='Pq9#tDF1')

    def test_user_create(self):
        url = reverse('signup')
        data = {'username': 'test_user_2', 'password': 'Pq9#tDF1', 'password_repeat': 'Pq9#tDF1'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)

    def test_user_login_success(self):
        url = reverse('signup')
        data = {'username': 'test_user_3', 'password': 'Pq9#tDF1', 'password_repeat': 'Pq9#tDF1'}
        _ = self.client.post(url, data, format='json')

        url = reverse('login')
        data = {'username': 'test_user_3', 'password': 'Pq9#tDF1'}
        res = self.client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)

    def test_show_user_profile(self):
        self.client.force_login(self.user)

        url = reverse('profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_obj = User.objects.get(pk=self.user.pk)
        self.assertEqual(user_obj.username, 'test_user')
        self.assertNotEqual(user_obj.username, self.superuser.username)

    def test_update_user_profile(self):
        self.client.force_login(self.user)

        url = reverse('profile')
        data = {
            'username': 'test_user',
            'first_name': 'Danya',
            'last_name': 'Manuilov',
            'email': 'manuilovdaniil@yandex.ru'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(pk=self.user.pk).count(), 1)

        user_obj = User.objects.get(pk=self.user.pk)
        self.assertEqual(user_obj.first_name, data['first_name'])
        self.assertEqual(user_obj.last_name, data['last_name'])
        self.assertEqual(user_obj.email, data['email'])

    def test_partial_update_user_profile(self):
        self.client.force_login(self.user)

        url = reverse('profile')
        data = {'first_name': 'Daniil'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(pk=self.user.pk).count(), 1)

        user_obj = User.objects.get(pk=self.user.pk)
        self.assertEqual(user_obj.first_name, data['first_name'])
        self.assertEqual(user_obj.username, 'test_user')
        self.assertEqual(user_obj.last_name, '')

    def test_delete_user(self):
        self.client.force_login(self.user)

        url = reverse('profile')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(pk=self.user.pk).count(), 1)

        url = reverse('profile')
        res_logout = self.client.get(url, format='json')
        self.assertEqual(res_logout.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_password(self):
        self.client.force_login(self.user)
        url = reverse('update_password')
        data = {'old_password': 'Pq9#tDF1', 'new_password': 'Pq9#tDF2'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(pk=self.user.pk).count(), 1)

        self.client.logout()
        url = reverse('login')
        data = {'username': self.user.username, 'password': 'Pq9#tDF2'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
