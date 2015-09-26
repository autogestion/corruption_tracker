# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0006_auto_20150926_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
