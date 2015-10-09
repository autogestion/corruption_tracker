# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0008_remove_claim_polygon_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=555)),
            ],
        ),
        migrations.RemoveField(
            model_name='incharge',
            name='organization_types',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='org_type',
        ),
        migrations.DeleteModel(
            name='OrganizationType',
        ),
        migrations.AddField(
            model_name='claim',
            name='claim_type',
            field=models.ForeignKey(to='claim.ClaimType', blank=True, default=None, null=True),
        ),
    ]
