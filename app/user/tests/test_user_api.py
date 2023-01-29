"""Test user api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests creating a user is successfull"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user successfully"""
        print("Starting test_create_user_success")
        payload = {
            'email': 'test@example.com',
            'password': '12345',
            'name': 'test'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned is user with wmail exists"""
        print("Starting test_user_with_email_exists_error")
        payload = {
            'email': 'test@exmaple.com',
            'password': 'testpass123',
            'name': 'test'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """test if error is returned when password is too short"""
        print("Starting test_password_too_short_error")
        payload = {
            'email': 'test@example.com',
            'passwrod': 'pw',
            'name': 'test'
        }

        res = self.client.port(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
