# -*- coding: utf-8 -*-
import datetime
import json

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class OrganizationType(models.Model):
    # TODO(autogestion) This data (ORG_TYPES) could be moved to separate
    # json file and loads to DB by initiate_db command together with
    # geojson wich contains organizations of this type

    # ORG_TYPES = (
    #     ("0", _("Unknown")),
    #     ("1", _("Міністерство фінансів України")),
    #     ("2", _("Міністерство соціальної політики України")),
    #     ("3", _("Міністерство регіонального розвитку, "
    #             "будівництва та житлово-комунального господарства України")),
    #     ("4", _("Міністерство охорони здоров'я України ")),
    #     ("5", _("Міністерство освіти і науки України")),
    #     ("6", _("Міністерство оборони України")),
    #     ("7", _("Міністерство молоді та спорту України")),
    #     ("8", _("Міністерство культури України")),
    #     ("9", _("Міністерство інфраструктури України")),
    #     ("10", _("Міністерство інформаційної політики України")),
    #     ("11", _("Міністерство закордонних справ України")),
    #     ("12", _("Міністерство енергетики та вугільної промисловості "
    #              "України")),
    #     ("13", _("Міністерство економічного розвитку і торгівлі України")),
    #     ("14", _("Міністерство екології та природних ресурсів України")),
    #     ("15", _("Міністерство внутрішніх справ України")),
    #     ("16", _("Міністерство аграрної політики та продовольства України")),
    #     ("17", _("Міністерство юстиції України")),
    # )
    # org_type = models.CharField(choices=ORG_TYPES,
    #                             max_length=10,
    #                             default=ORG_TYPES[0][0],
    #                             unique=True)

    # Now for example we need to add election station type,
    # so need to change source. Better if type would be parsed
    # from json or add through admin
    # TODO(vegasq) should we use AMENITY as keys here?
    type_id = models.CharField(primary_key=True, max_length=155)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_id

    # def __str__(self):
    #     for org_type in self.ORG_TYPES:
    #         if org_type[0] == str(self.org_type):
    #             return org_type[1]


class ClaimType(models.Model):
    """
    Binding the set of ClaimType objects to OrganizationType
    allow to show to user dropdown with common violations
    in organizations of certain type

    """
    name = models.CharField(max_length=555)
    org_type = models.ManyToManyField(OrganizationType)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    org_type = models.ForeignKey(OrganizationType, null=True, blank=True)

    @property
    def total_claims(self):
        return self.claim_set.all().count()

    def json_claims(self):
        claims = self.claim_set.all()

        claims_list = []

        if claims:
            for claim in claims:

                claim_type = claim.claim_type.name if\
                    claim.claim_type else _('Others')
                username = claim.complainer.username if\
                    claim.complainer else _("Anon")
                claims_list.append({
                    'organization_id': self.id,
                    'organization_name': self.name,
                    'text': claim.text,
                    'servant': claim.servant,
                    'complainer': username,
                    'claim_type': claim_type
                })

        return json.dumps(claims_list)

    def __str__(self):
        return self.name


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
    servant = models.CharField(max_length=550)
    complainer = models.ForeignKey(User, null=True, blank=True, default=None)
    claim_type = models.ForeignKey(ClaimType, null=True, blank=True,
                                   default=None)
