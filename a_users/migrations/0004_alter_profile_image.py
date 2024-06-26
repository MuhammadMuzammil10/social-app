# Generated by Django 5.0.4 on 2024-05-14 15:49

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0003_remove_profile_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=85, scale=None, size=[600, 600], upload_to='avatars/'),
        ),
    ]
