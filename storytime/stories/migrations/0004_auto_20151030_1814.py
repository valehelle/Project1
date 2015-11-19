# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20151030_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='small',
            field=models.FileField(default=b'none', upload_to=storytime.stories.models.get_upload_file_name),
        ),
    ]
