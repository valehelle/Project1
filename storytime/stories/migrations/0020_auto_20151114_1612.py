# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0019_auto_20151114_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='profile_pic',
            field=models.ImageField(default=b'media/default/UserIconBlack.png', upload_to=storytime.stories.models.get_upload_file_name),
        ),
    ]
