# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_remove_image_small'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='source',
            field=models.ImageField(upload_to=storytime.stories.models.get_upload_file_name),
        ),
    ]
