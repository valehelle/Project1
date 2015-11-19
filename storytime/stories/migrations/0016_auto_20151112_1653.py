# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0015_auto_20151106_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=500)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RenameField(
            model_name='story',
            old_name='star',
            new_name='starcount',
        ),
        migrations.AlterField(
            model_name='image',
            name='storyid',
            field=models.ForeignKey(to='stories.Story'),
        ),
        migrations.AlterField(
            model_name='text',
            name='storyid',
            field=models.ForeignKey(to='stories.Story'),
        ),
        migrations.AddField(
            model_name='star',
            name='storyid',
            field=models.ForeignKey(to='stories.Story'),
        ),
        migrations.AddField(
            model_name='star',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='storyid',
            field=models.ForeignKey(to='stories.Story'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
