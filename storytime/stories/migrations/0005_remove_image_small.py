# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_auto_20151030_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='small',
        ),
    ]
