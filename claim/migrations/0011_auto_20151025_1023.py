# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


class Migration(migrations.Migration):

    def run_initial(apps, schema_editor):
        call_command('loaddata', 'initial_data')

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
        migrations.RunPython(run_initial),
        migrations.AddField(
            model_name='claim',
            name='moderation',
            field=models.ForeignKey(to='claim.ModerationStatus', default='not_moderated'),
        ),
    ]
