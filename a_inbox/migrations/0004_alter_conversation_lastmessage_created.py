# Generated by Django 5.0.4 on 2024-05-08 06:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_inbox', '0003_alter_conversation_is_seen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='lastmessage_created',
            field=models.DateField(default=datetime.datetime(2024, 5, 8, 6, 34, 41, 130989, tzinfo=datetime.timezone.utc)),
        ),
    ]