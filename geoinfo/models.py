import json

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from claim.models import Organization, OrganizationType


class Layer(models.Model):
    """
        Representation of GeoJSON.
        Is a collection of polygons, united on the
        basis of type and proximity
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
    is_default = models.BooleanField(default=False)
    zoom = models.IntegerField()
    center = models.CharField(max_length=50)

    # @property
    # def max_claims(self):
    #     return max([x.total_claims for x in self.polygon_set.all()])

    def color_spot(self, value, max_value):
        percent = value * 100 / max_value

        if percent <= 20:
            return 'green'
        elif percent <= 70:
            return 'yellow'
        else:
            return 'red'

    def generate_json(self, add=False):
        polygons = self.polygon_set.all()
        max_claims_value = max([x.total_claims for x in polygons])

        data = []
        organizations = []
        for polygon in polygons:
            polygon_json = polygon.generate_map_polygon()
            polygon_claims = polygon_json["properties"]['polygon_claims']
            polygon_json["properties"]['color'] = self.color_spot(
                polygon_claims, max_claims_value)\
                if polygon_claims else 'grey'
            data.append(polygon_json)
            organizations.extend(polygon.organizations.all())

        places = [{'data': org.id,
                  'value': org.name,
                   'org_type_id': org.org_type.type_id if org.org_type else 0}
                  for org in organizations]

        geo_json = {
            'type': "FeatureCollection",
            'config': {
                'center': json.loads(self.center),
                'zoom': self.zoom},
        }
        geo_json['features'] = data

        responce = {'buildings': mark_safe(json.dumps(geo_json)),
                    'places': mark_safe(json.dumps(places))}

        if add:
            org_types = OrganizationType.objects.filter(
                type_id__in=list(set([x['org_type_id'] for x in places])))

            claim_type_sets = {}
            for org_type in org_types:
                claim_type_set = []
                for claim_type in org_type.claimtype_set.all():
                    claim_type_set.append({'id': claim_type.id,
                                          'value': claim_type.name})
                claim_type_sets[org_type.type_id] = claim_type_set

            responce['claim_types'] = mark_safe(json.dumps(claim_type_sets))

        return responce

    def __str__(self):
        return self.name


class Polygon(models.Model):
    # TODO(vegasq) Let's pretend that Polygon represent
    # building, but Polygon.organizations - list of offices.
    polygon_id = models.IntegerField(primary_key=True)
    organizations = models.ManyToManyField(Organization)
    layer = models.ForeignKey(Layer)
    shape = models.CharField(max_length=2000)
    centroid = models.CharField(max_length=50, null=True, blank=True)

    @property
    def total_claims(self):
        return sum([x.total_claims for x in self.organizations.all()])

    def generate_map_polygon(self):
        orgs = []
        polygon_claims = 0
        for org in self.organizations.all():
            org_claims = org.claim_set.all().count()
            polygon_claims += org_claims
            orgs.append({'id': org.id,
                        'name': org.name,
                         'claims_count': org_claims})

        # reverse coordinates for manualy adding polgygons
        geometry = json.loads(self.shape)
        [x.reverse() for x in geometry["coordinates"][0]]
        centroid = json.loads(self.centroid)
        centroid.reverse()

        return {
            "type": "Feature",
            "properties": {
                "ID": self.polygon_id,
                "organizations": orgs,
                "centroid": centroid,
                "polygon_claims": polygon_claims
            },
            "geometry": geometry
        }

    def organization_count(self):
        return self.organizations.all().count()

    def __str__(self):
        return 'Polygon ' + str(self.polygon_id)
