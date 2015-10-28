# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0007_polygon_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polygon',
            name='shape',
            field=models.CharField(max_length=10000),
        ),
    ]
