# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import storytime.stories.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20151003_1119'),
        ('stories', '0006_auto_20151102_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.ManyToManyField(to='stories.Subscriber')),
            ],
        ),
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('desc', models.CharField(max_length=200)),
                ('profile_pic', models.ImageField(upload_to=storytime.stories.models.get_upload_file_name)),
            ],
        ),
    ]
