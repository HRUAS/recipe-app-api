"""
Test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


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
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Tests if that tries to create a user without email"""
        print("Starting test_new_user_without_email_raises_error")
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        print("Starting test_create_superuser")
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successfully"""
        print("Starting test_create_recipe")
        user = get_user_model().objects.create_user(
            'test@example.com',
            'password'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minute=5,
            price=Decimal('5.50'),
            description='Sample Recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)
