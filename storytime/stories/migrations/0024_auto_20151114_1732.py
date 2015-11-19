# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0023_auto_20151114_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile_image',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_info',
            name='profile_pic',
        ),
        migrations.RemoveField(
            model_name='user_info',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile_Image',
        ),
        migrations.DeleteModel(
            name='User_Info',
        ),
    ]
