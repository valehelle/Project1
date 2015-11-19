# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0020_auto_20151114_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'media/default/UserIconBlack.png', upload_to=storytime.stories.models.get_upload_file_name)),
                ('used', models.BooleanField(default=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='user_info',
            name='profile_pic',
            field=models.ForeignKey(to='stories.Profile_Image'),
        ),
    ]
