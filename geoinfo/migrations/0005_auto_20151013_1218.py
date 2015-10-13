# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0004_auto_20151004_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='layer',
            old_name='json_filename',
            new_name='json_file',
        ),
        migrations.AddField(
            model_name='layer',
            name='parse_file',
            field=models.BooleanField(default=False),
        ),
    ]
