# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordquiz', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clue', models.CharField(max_length=200)),
                ('img', models.ForeignKey(to='wordquiz.MediaObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
