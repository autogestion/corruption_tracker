# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 22:34
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2550)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('live', models.BooleanField(default=False)),
                ('servant', models.CharField(max_length=550)),
                ('moderation', models.CharField(choices=[('not_moderated', 'Not moderated'), ('suspicious', 'Suspicious'), ('anonymous', 'From anonymous'), ('valid', 'Moderated')], default='not_moderated', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClaimType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=555)),
                ('icon', models.FileField(blank=True, null=True, upload_to='icons/')),
            ],
        ),
        migrations.CreateModel(
            name='InCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_claims', multiselectfield.db.fields.MultiSelectField(choices=[('not_moderated', 'Not moderated'), ('suspicious', 'Suspicious'), ('anonymous', 'From anonymous'), ('valid', 'Moderated')], default='not_moderated,suspicious,anonymous,valid', max_length=40)),
                ('use_memcached', models.BooleanField(default=False)),
                ('memcached_timeout', models.IntegerField(default=3600)),
                ('claims_per_hour', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name_plural': 'Moderator',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('type_id', models.CharField(max_length=155, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='claim.OrganizationType'),
        ),
        migrations.AddField(
            model_name='incharge',
            name='organization_types',
            field=models.ManyToManyField(to='claim.OrganizationType'),
        ),
        migrations.AddField(
            model_name='incharge',
            name='organizations',
            field=models.ManyToManyField(to='claim.Organization'),
        ),
        migrations.AddField(
            model_name='claimtype',
            name='org_type',
            field=models.ManyToManyField(to='claim.OrganizationType'),
        ),
        migrations.AddField(
            model_name='claim',
            name='claim_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='claim.ClaimType'),
        ),
        migrations.AddField(
            model_name='claim',
            name='complainer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='claim',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claim.Organization'),
        ),
    ]
