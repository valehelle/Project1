# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0029_star_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='commentcount',
            field=models.IntegerField(default=0),
        ),
    ]
