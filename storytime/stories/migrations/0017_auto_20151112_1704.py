# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0016_auto_20151112_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='storyid',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
