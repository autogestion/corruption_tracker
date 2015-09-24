# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0003_organization_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('layer_type', models.IntegerField(default=0, choices=[(0, 'Organization'), (1, 'District'), (2, 'Country')])),
            ],
        ),
        migrations.CreateModel(
            name='Polygon',
            fields=[
                ('polygon_id', models.IntegerField(serialize=False, primary_key=True)),
                ('coordinates', models.CharField(max_length=2000)),
                ('layer', models.ForeignKey(to='claim.Layer')),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(to='claim.OrganizationType', null=True),
        ),
        migrations.AddField(
            model_name='polygon',
            name='organizations',
            field=models.ManyToManyField(to='claim.Organization'),
        ),
    ]
