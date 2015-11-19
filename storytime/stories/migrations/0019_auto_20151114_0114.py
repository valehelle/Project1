# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0018_story_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='name',
            new_name='username',
        ),
    ]
