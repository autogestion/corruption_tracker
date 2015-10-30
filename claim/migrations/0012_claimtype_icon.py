# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0011_auto_20151025_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimtype',
            name='icon',
            field=models.FileField(blank=True, upload_to='icons/', null=True),
        ),
    ]
