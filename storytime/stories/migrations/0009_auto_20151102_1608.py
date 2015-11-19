# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0008_auto_20151102_0322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='person',
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]
