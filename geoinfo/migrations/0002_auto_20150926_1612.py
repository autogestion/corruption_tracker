# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='layer',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
