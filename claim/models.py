# -*- coding: utf-8 -*-
import datetime

from django.db import models, connection
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.cache import cache

from multiselectfield import MultiSelectField

from claim.sql import moderation_filter

STATUSES = (('not_moderated', _('Not moderated')),
            ('suspicious', _('Suspicious')),
            ('anonymous', _('From anonymous')),
            ('valid', _('Moderated')),
            ('markers', _('Non-verified markers'))
            )


class Moderator(models.Model):
    """
    Singleton model, where admin can choose
    claims with wich state of moderation to show

    """

    show_claims = MultiSelectField(choices=STATUSES, max_length=200,
        default='not_moderated,suspicious,anonymous,valid')

    # memcached settings
    use_memcached = models.BooleanField(default=False)
    memcached_timeout = models.IntegerField(default=3600)
    claims_per_hour = models.IntegerField(default=3)

    class Meta:
        verbose_name_plural = "Moderator"

    def save(self, *args, **kwargs):
        self.id = 1
        super(Moderator, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_moderator(cls):
        return cls.objects.get(id=1)

    @classmethod
    def allowed_statuses(cls):
        return cls.objects.get(id=1).show_claims


class OrganizationType(models.Model):
    type_id = models.CharField(primary_key=True, max_length=155)
    name = models.CharField(max_length=255)

    def claim_types(self):
        claim_types = self.claimtype_set.all()
        claim_types_list = []

        for claim_type in claim_types:
            claim_types_list.append({
                'id': claim_type.id,
                'name': claim_type.name,
                'icon': claim_type.icon.url if\
                claim_type.icon else False
            })
        return claim_types_list

    def __str__(self):
        return self.type_id


class ClaimType(models.Model):
    """
    Binding the set of ClaimType objects to OrganizationType
    allow to show to user dropdown with common violations
    in organizations of certain type

    """
    name = models.CharField(max_length=555)
    org_type = models.ManyToManyField(OrganizationType)
    icon = models.FileField(upload_to='icons/', null=True, blank=True)

    def __str__(self):
        return self.name

    def linked_org_types(self):
        return ','.join([x.type_id for x in self.org_type.all()])


class AddressException(Exception):
    pass


class Organization(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    org_type = models.ForeignKey(OrganizationType, null=True, blank=True)

    is_verified = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    def moderation_filter(self):
        return self.claim_set.filter(
            moderation__in=Moderator.allowed_statuses())

    def first_polygon(self):
        try:
            return self.polygon_set.all()[0]
        except IndexError:
            return None

    def polygons(self):
        polygons = None
        cached = cache.get('polygons_for::%s' % self.id)
        if cached is not None:
            polygons = cached
        else:
            polygons = self.polygon_set.all().values_list('polygon_id', flat=True)
            cache.set('polygons_for::%s' % self.id, polygons, 300)

        return polygons

    def address(self):
        try:
            cached = cache.get('address_for::%s' % self.id)
            if cached is not None:
                address = cached
            else:
                address = self.polygon_set.all()[0].address
                cache.set('address_for::%s' % self.id, address, 300)

            return address
        except IndexError:
            raise AddressException

    @property
    def claims(self):
        # return self.moderation_filter().count()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS __count FROM claim_claim WHERE 
                (claim_claim.organization_id = %d AND %s );                   
            """ % (self.id, moderation_filter))

        return cursor.fetchone()[0]
  
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
    moderation = models.CharField(choices=STATUSES, max_length=50,
                                  default='not_moderated')
    bribe = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Claim, self).save(*args, **kwargs)
        key = 'color_for::%s' % self.organization.first_polygon().polygon_id
        if cache.has_key(key):
            cache.delete(key)
