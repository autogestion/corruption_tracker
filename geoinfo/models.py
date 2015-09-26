import json

from django.db import models
from django.utils.translation import ugettext as _

from claim.models import Organization, Claim


# TODO(autogestion) Maybe we have to create separate app,
# wich would handle geo info and will contain
# Layer and Polygon models
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

    # TODO(autogestion) name should be uniqe=True?
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
        claims_count = 0
        for org in self.organizations.all():
            orgs.append(org.get_map_representation())
            claims_count += org.total_claims

        names = " <br> ".join([org['name'] for org in orgs])

        return {
            "type": "Feature",
            "properties": {
                "ID": self.polygon_id,
                "NAME": names,
                "ORGANIZATIONS": orgs,
                "CLAIM_COUNT": claims_count
            },
            "geometry": json.loads(self.coordinates)
        }

    def get_json_claims(self):
        # Q(polygon_id=self.id) jsut compatible layer.
        # Remove me after release. Not critical.
        claims = Claim.objects.filter(
            organization__in=self.organizations.all())
        claims_list = []

        if claims:
            for claim in claims:
                username = claim.complainer.username if\
                    claim.complainer else _("Anon")
                claims_list.append({
                    'organization_id': claim.organization.id,
                    'organization_name': claim.organization.name,
                    'text': claim.text,
                    'servant': claim.servant,
                    'complainer': username
                })

        return json.dumps(claims_list)

    def __str__(self):
        return 'Polygon ' + str(self.polygon_id)
