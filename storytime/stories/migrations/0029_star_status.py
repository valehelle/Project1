# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0028_auto_20151116_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='star',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
