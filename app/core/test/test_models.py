"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """ Tests models"""

    def test_create_user_with_email_successful(self):
        """test to create a user with mail"""
        print("Starting test_create_user_with_email_successful")
        email = "test@example.com"
        password = "testpass1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if email has been normalized"""
        print("Starting test_new_user_email_normalized")
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test@Example.com', 'Test@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
