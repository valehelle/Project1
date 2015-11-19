# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0017_auto_20151112_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
