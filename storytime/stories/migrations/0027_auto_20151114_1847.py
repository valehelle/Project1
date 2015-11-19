# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0026_auto_20151114_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='username',
        ),
        migrations.RemoveField(
            model_name='text',
            name='username',
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
