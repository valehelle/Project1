# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0025_auto_20151114_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='profile_pic',
            field=models.ForeignKey(to='stories.Profile_Image', null=True),
        ),
    ]
