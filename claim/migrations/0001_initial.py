# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.CharField(max_length=2550)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('live', models.BooleanField(default=False)),
                ('polygon_id', models.CharField(max_length=250)),
                ('servant', models.CharField(max_length=550)),
                ('complainer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
