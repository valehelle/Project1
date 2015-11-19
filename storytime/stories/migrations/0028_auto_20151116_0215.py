# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0027_auto_20151114_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='starcount',
            field=models.IntegerField(default=0),
        ),
    ]
