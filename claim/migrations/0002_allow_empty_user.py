# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='complainer',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
