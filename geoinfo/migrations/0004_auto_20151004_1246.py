# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0003_auto_20151003_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='center',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='layer',
            name='zoom',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
