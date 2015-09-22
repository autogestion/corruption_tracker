# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0002_allow_empty_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='InCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('org_type', models.CharField(max_length=10, default='0', choices=[('0', 'Unknown'), ('1', 'Міністерство фінансів України'), ('2', 'Міністерство соціальної політики України'), ('3', 'Міністерство регіонального розвитку, будівництва та житлово-комунального господарства України'), ('4', "Міністерство охорони здоров'я України "), ('5', 'Міністерство освіти і науки України'), ('6', 'Міністерство оборони України'), ('7', 'Міністерство молоді та спорту України'), ('8', 'Міністерство культури України'), ('9', 'Міністерство інфраструктури України'), ('10', 'Міністерство інформаційної політики України'), ('11', 'Міністерство закордонних справ України'), ('12', 'Міністерство енергетики та вугільної промисловості України'), ('13', 'Міністерство економічного розвитку і торгівлі України'), ('14', 'Міністерство екології та природних ресурсів України'), ('15', 'Міністерство внутрішніх справ України'), ('16', 'Міністерство аграрної політики та продовольства України'), ('17', 'Міністерство юстиції України')])),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(to='claim.OrganizationType'),
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
            model_name='claim',
            name='organization',
            field=models.ForeignKey(default=0, to='claim.Organization'),
            preserve_default=False,
        ),
    ]
