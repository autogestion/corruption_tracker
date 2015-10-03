# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0002_auto_20150926_1612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='polygon',
            old_name='coordinates',
            new_name='shape',
        ),
        migrations.AddField(
            model_name='polygon',
            name='centroid',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
