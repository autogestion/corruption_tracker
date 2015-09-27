import json

from django.db import models
from django.utils.translation import ugettext as _

from claim.models import Organization


class Layer(models.Model):
    """
        Some general representation of map.
        f.e.
            All schools of Lviv
            All universities of Ukraine
            etc.
    """
    ORGANIZATION = 0
    DISTRICT = 1
    COUNTRY = 2
    LAYER_TYPES = (
        (ORGANIZATION, _("Organization")),
        (DISTRICT, _("District")),
        (COUNTRY, _("Country")),
    )

    name = models.CharField(max_length=250, unique=True)
    layer_type = models.IntegerField(choices=LAYER_TYPES,
                                     default=ORGANIZATION)

    # TODO(autogestion) This field will allow to upload
    # geojson files through admin
    json_filename = models.FileField(null=True, blank=True)

    # If field set to True,
    # this Layer would be loaded on main page
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Polygon(models.Model):
    # TODO(vegasq) Let's pretend that Polygon represent
    # building, but Polygon.organizations - list of offices.
    polygon_id = models.IntegerField(primary_key=True)
    organizations = models.ManyToManyField(Organization)
    layer = models.ForeignKey(Layer)
    coordinates = models.CharField(max_length=2000)

    def generate_map_polygon(self):
        orgs = []
        for org in self.organizations.all():
            orgs.append({'id': org.id,
                        'name': org.name,
                         'claims_count': org.claim_set.all().count()})

        return {
            "type": "Feature",
            "properties": {
                "ID": self.polygon_id,
                "ORGANIZATIONS": orgs,
            },
            "geometry": json.loads(self.coordinates)
        }

    def organization_count(self):
        return self.organizations.all().count()

    def __str__(self):
        return 'Polygon ' + str(self.polygon_id)
