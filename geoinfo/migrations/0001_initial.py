# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0006_auto_20150926_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('layer_type', models.IntegerField(choices=[(0, 'Organization'), (1, 'District'), (2, 'Country')], default=0)),
                ('json_filename', models.FileField(blank=True, upload_to='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Polygon',
            fields=[
                ('polygon_id', models.IntegerField(primary_key=True, serialize=False)),
                ('coordinates', models.CharField(max_length=2000)),
                ('layer', models.ForeignKey(to='geoinfo.Layer')),
                ('organizations', models.ManyToManyField(to='claim.Organization')),
            ],
        ),
    ]
