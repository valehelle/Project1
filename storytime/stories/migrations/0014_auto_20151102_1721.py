# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0013_auto_20151102_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
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
    ]
