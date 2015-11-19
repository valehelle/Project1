# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0010_auto_20151102_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='relationships',
        ),
        migrations.RemoveField(
            model_name='person',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='from_person',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='to_person',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='Relationship',
        ),
    ]
