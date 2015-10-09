# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0009_auto_20151008_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('type_id', models.CharField(max_length=155, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='claimtype',
            name='org_type',
            field=models.ManyToManyField(to='claim.OrganizationType'),
        ),
        migrations.AddField(
            model_name='incharge',
            name='organization_types',
            field=models.ManyToManyField(to='claim.OrganizationType'),
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(null=True, blank=True, to='claim.OrganizationType'),
        ),
    ]
