# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0009_auto_20151102_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(choices=[(1, b'Following'), (2, b'Blocked')])),
                ('from_person', models.ForeignKey(related_name='from_people', to='stories.Person')),
                ('to_person', models.ForeignKey(related_name='to_people', to='stories.Person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='relationships',
            field=models.ManyToManyField(related_name='related_to', through='stories.Relationship', to='stories.Person'),
        ),
        migrations.AddField(
            model_name='person',
            name='userid',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
