# Generated by Django 2.2.1 on 2020-02-10 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surfer', '0002_commentcomment_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowEditor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor_list', models.ManyToManyField(related_name='Editor', to=settings.AUTH_USER_MODEL)),
                ('surfer_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]