# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20151003_1119'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0022_auto_20151114_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'media/default/UserIconBlack.png', upload_to=storytime.stories.models.get_upload_file_name)),
                ('used', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('username', models.CharField(max_length=200)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('desc', models.CharField(max_length=200)),
                ('profile_pic', models.ForeignKey(to='stories.Profile_Image')),
            ],
        ),
        migrations.AddField(
            model_name='profile_image',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
