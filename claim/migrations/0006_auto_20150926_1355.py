# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0005_auto_20150925_0649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polygon',
            name='layer',
        ),
        migrations.RemoveField(
            model_name='polygon',
            name='organizations',
        ),
        migrations.DeleteModel(
            name='Layer',
        ),
        migrations.DeleteModel(
            name='Polygon',
        ),
    ]
