# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0011_auto_20151025_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderator',
            name='claims_per_hour',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='moderator',
            name='memcached_timeout',
            field=models.IntegerField(default=3600),
        ),
        migrations.AddField(
            model_name='moderator',
            name='use_memcached',
            field=models.BooleanField(default=False),
        ),
    ]
