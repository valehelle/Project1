# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.FileField(upload_to=storytime.stories.models.get_upload_file_name)),
                ('position', models.IntegerField(default=0)),
                ('storyid', models.UUIDField(default=uuid.uuid4)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('star', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=200)),
                ('storyid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('position', models.IntegerField(default=0)),
                ('storyid', models.UUIDField(default=uuid.uuid4)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
    ]
