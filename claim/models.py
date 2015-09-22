# -*- coding: utf-8 -*-
import datetime
import json

from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.translation import ugettext as _


class OrganizationType(models.Model):
    # TODO(vegasq) should we use AMENITY as keys here?
    ORG_TYPES = (
        ("0", _("Unknown")),
        ("1", _("Міністерство фінансів України")),
        ("2", _("Міністерство соціальної політики України")),
        ("3", _("Міністерство регіонального розвитку, "
                "будівництва та житлово-комунального господарства України")),
        ("4", _("Міністерство охорони здоров'я України ")),
        ("5", _("Міністерство освіти і науки України")),
        ("6", _("Міністерство оборони України")),
        ("7", _("Міністерство молоді та спорту України")),
        ("8", _("Міністерство культури України")),
        ("9", _("Міністерство інфраструктури України")),
        ("10", _("Міністерство інформаційної політики України")),
        ("11", _("Міністерство закордонних справ України")),
        ("12", _("Міністерство енергетики та вугільної промисловості "
                 "України")),
        ("13", _("Міністерство економічного розвитку і торгівлі України")),
        ("14", _("Міністерство екології та природних ресурсів України")),
        ("15", _("Міністерство внутрішніх справ України")),
        ("16", _("Міністерство аграрної політики та продовольства України")),
        ("17", _("Міністерство юстиції України")),
    )
    org_type = models.CharField(choices=ORG_TYPES,
                                max_length=10,
                                default=ORG_TYPES[0][0])

    def __str__(self):
        for org_type in self.ORG_TYPES:
            if org_type[0] == str(self.org_type):
                return org_type[1]


class Organization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    org_type = models.ForeignKey(OrganizationType)

    def __str__(self):
        return self.name

    def get_json_claims(self):
        # Q(polygon_id=self.id) jsut compatible layer.
        # Remove me after release. Not critical.
        claims = Claim.objects.filter(Q(organization=self) |
                                      Q(polygon_id=self.id))
        claims_list = []

        if claims:
            for claim in claims:
                username = claim.complainer.username if\
                    claim.complainer else _("Anon")
                claims_list.append({
                    'text': claim.text,
                    'servant': claim.servant,
                    'complainer': username
                })

        return json.dumps(claims_list)


class InCharge(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    organizations = models.ManyToManyField(Organization)
    organization_types = models.ManyToManyField(OrganizationType)

    def __str__(self):
        return self.name


class Claim(models.Model):
    text = models.CharField(max_length=2550)
    created = models.DateTimeField(default=datetime.datetime.now)
    live = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization)
    polygon_id = models.CharField(max_length=250)
    servant = models.CharField(max_length=550)
    complainer = models.ForeignKey(User, null=True, blank=True, default=None)

    @classmethod
    def update_map(cls, json_data):
        """
        Update map with claim information
        """
        polygons_values = cls.objects.values('polygon_id').\
            annotate(count=Count('polygon_id'))

        polygons_dict = {}
        for values_dict in polygons_values:
            polygons_dict[values_dict['polygon_id']] = values_dict['count']

        for polygon in json_data["features"]:
            polygon['claim_count'] = polygons_dict.get(
                str(polygon["properties"]["ID"]), 0)
