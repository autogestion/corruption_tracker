# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0012_claimtype_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='moderation',
            field=models.CharField(default='not_moderated', choices=[('not_moderated', 'Not moderated'), ('suspicious', 'Suspicious'), ('anonymous', 'From anonymous'), ('valid', 'Moderated')], max_length=50),
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='show_claims',
        ),
        migrations.AddField(
            model_name='moderator',
            name='show_claims',
            field=multiselectfield.db.fields.MultiSelectField(default='not_moderated,suspicious,anonymous,valid', choices=[('not_moderated', 'Not moderated'), ('suspicious', 'Suspicious'), ('anonymous', 'From anonymous'), ('valid', 'Moderated')], max_length=40),
        ),
        migrations.DeleteModel(
            name='ModerationStatus',
        ),
    ]
