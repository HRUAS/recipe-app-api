# Generated by Django 3.2.16 on 2023-01-31 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='users',
            new_name='user',
        ),
    ]
