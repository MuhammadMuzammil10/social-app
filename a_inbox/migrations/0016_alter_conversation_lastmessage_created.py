# Generated by Django 5.0.4 on 2024-05-30 21:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_inbox', '0015_alter_conversation_lastmessage_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='lastmessage_created',
            field=models.DateField(default=datetime.datetime(2024, 5, 30, 21, 23, 53, 505340, tzinfo=datetime.timezone.utc)),
        ),
    ]
