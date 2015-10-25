# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0010_auto_20151008_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationStatus',
            fields=[
                ('status_id', models.CharField(max_length=155, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('show_claims', models.ManyToManyField(to='claim.ModerationStatus')),
            ],
            options={
                'verbose_name_plural': 'Moderator',
            },
        ),
        migrations.AddField(
            model_name='claim',
            name='moderation',
            field=models.ForeignKey(to='claim.ModerationStatus', default='not_moderated'),
        ),
    ]
