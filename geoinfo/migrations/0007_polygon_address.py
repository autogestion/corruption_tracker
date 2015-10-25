# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0006_auto_20151014_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='polygon',
            name='address',
            field=models.CharField(blank=True, null=True, max_length=800),
        ),
    ]
