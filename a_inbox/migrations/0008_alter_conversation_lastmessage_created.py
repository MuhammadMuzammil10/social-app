# Generated by Django 5.0.4 on 2024-05-12 08:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_inbox', '0007_alter_conversation_lastmessage_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='lastmessage_created',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 8, 4, 28, 327813, tzinfo=datetime.timezone.utc)),
        ),
    ]
