"""Test user api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Generates token for added credentials"""
        print("Starting test_create_token_for_user")
        user_details = {
            'name': 'test_name',
            'email': 'test@example.com',
            'password': '123456'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Tests return error if credential are invalid"""
        print("Starting test_create_token_bad_credentials")
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        print("Starting test_create_token_blank_password")
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_unautharized(self):
        """Test authentication for user"""
        print("Starting test_user_unautharized")
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests API request that require authentication"""

    def setUP(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """Test retriving profile from logged in user"""
        print("Starting test_retrive_profile_success")
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.name,
        })

    def test_post_me_not_allowed(self):
        """Test post is not allowed for the me endpoint"""
        print("Starting test_post_me_not_allowed")
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_MTHEOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Tests Updating the user profile for the authenticated user"""
        print("Starting test_update_user_profile")
        payload = {'name': 'updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
