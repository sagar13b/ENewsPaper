# Generated by Django 3.0.2 on 2020-02-07 10:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentcomment',
            name='comment',
            field=models.CharField(default=datetime.datetime(2020, 2, 7, 10, 57, 2, 165887, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
    ]