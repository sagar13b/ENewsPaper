# Generated by Django 2.2.1 on 2020-02-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_editorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorprofile',
            name='no_followers',
            field=models.IntegerField(default=0),
        ),
    ]
