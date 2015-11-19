# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import storytime.stories.models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_image_small'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='small',
            field=sorl.thumbnail.fields.ImageField(default=b'none', upload_to=storytime.stories.models.get_upload_file_name),
        ),
    ]
