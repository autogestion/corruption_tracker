# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0005_auto_20151013_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='json_file',
            field=models.FileField(upload_to='geojsons', blank=True, null=True),
        ),
    ]
