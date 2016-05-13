import json
from pprint import pprint

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
# from django.utils.safestring import mark_safe
from django.core.cache import cache

# from claim.models import Organization, OrganizationType, Moderator
from claim.models import Organization


class Uploader(models.Model):

    json_file = models.FileField(upload_to='geojsons')

    def save(self, *args, **kwargs):
        if self.json_file:
            from utils.geoparser import GeoJSONParser
            geojson = json.loads(self.json_file.read().decode('utf8'))
            GeoJSONParser.geojson_to_db(geojson)

    def __str__(self):
        return self.json_file.name

    class Meta:
        verbose_name_plural = "Uploader"


class Polygon(models.Model):
    """
    Polygon represent geo object,
    and could refer to collection of lower polygons
    """

    # Polygon as polygon
    polygon_id = models.CharField(max_length=50, primary_key=True)
    organizations = models.ManyToManyField(Organization, blank=True)
    shape = models.PolygonField(null=True, blank=True)
    centroid = models.PointField(null=True, blank=True)
    address = models.CharField(max_length=800, null=True, blank=True)
    layer = models.ForeignKey('self', blank=True, null=True)

    # Polygon as layer
    country = 0
    region = 1
    area = 2
    district = 3
    building = 4
    LEVEL = (
        (country, _("Root polygon")),
        (region, _("Regions of country")),
        (area, _("Subregions or big sities")),
        (district, _("Towns or districts of city")),
        (building, _("Houses"))
    )
    level = models.IntegerField(choices=LEVEL, default=building)
    is_verified = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    # outdated fields
    is_default = models.BooleanField(default=False)
    zoom = models.IntegerField(blank=True, null=True)

    claims = models.IntegerField(default=0)

    objects = models.GeoManager()

    @property
    def total_claims(self):
        claims = 0
        if self.level == self.building:
            claims += sum([x.claims for x in self.organizations.all()])

        else:
            cached = cache.get('claims_for::%s' % self.polygon_id)
            if cached is not None:
                claims = cached
            else:
                childs = self.polygon_set.all()
                for child in childs:
                    claims += child.total_claims

                cache.set('claims_for::%s' % self.polygon_id, claims)

        return claims

    def color_spot(self, value, max_value):
        if max_value:
            percent = value * 100 / max_value
        else:
            percent = 0

        if percent <= 20:
            return 'green'
        elif percent <= 70:
            return 'yellow'
        else:
            return 'red'

    @property
    def get_color(self):
        cached = cache.get('color_for::%s' % self.polygon_id)
        if cached is not None:
            color = cached
        else:
            if self.layer:
                brothers = self.layer.polygon_set.all()
                max_claims_value = max([x.total_claims for x in brothers])
            else:
                max_claims_value = 0

            color = self.color_spot(
                self.total_claims, max_claims_value)\
                if self.total_claims else 'grey'

            cache.set('color_for::%s' % self.polygon_id, color)

        return color

    # def orgs_count(self):
    #     return self.organizations.all().count()

    def first_organization(self):
        orgs = self.organizations.all()
        if orgs:
            return orgs[0]
        else:
            return None

    def __str__(self):
        return 'Polygon ' + str(self.polygon_id)

    def polygon_to_json(self, shape=True):
        # reverse coordinates for manualy adding polgygons
        if shape and self.shape:
            geometry = json.loads(self.shape.json)
            [x.reverse() for x in geometry["coordinates"][0]]
        else:
            geometry = None

        centroid = list(self.centroid.coords)
        centroid.reverse()

        responce = {
            "type": "Feature",
            "properties": {
                "ID": self.polygon_id,
                "centroid": centroid,
                'address': self.address,
                'parent_id': self.layer.polygon_id if self.layer else None,
                'level': self.level,
                # "polygon_claims": self.claims
            },
            "geometry": geometry
        }

        if self.level == self.building:
            orgs = []
            polygon_claims = 0
            for org in self.organizations.all():
                org_claims = org.claims
                polygon_claims += org_claims
                orgs.append({'id': org.id,
                            'name': org.name,
                             'claims_count': org_claims,
                             # 'claim_types': org.claim_types()
                             'org_type_id': org.org_type.type_id
                             })

            responce["properties"]["organizations"] = orgs
            responce["properties"]["polygon_claims"] = polygon_claims

        else:
            responce["properties"]["polygon_claims"] = self.total_claims

        # print(responce)
        return responce

    # def generate_childs(self, add=False):
    #     moderate = 'show_markers' in Moderator.objects.get(id=1).show_claims
    #     if moderate:
    #         polygons = self.polygon_set.filter(is_verified=True)
    #     else:
    #         polygons = self.polygon_set.all()

    #     responce = {}
    #     # if not polygons:
    #     #     return responce
    #     max_claims_value = max([x.total_claims for x in polygons])

    #     data = []
    #     places = []
    #     for polygon in polygons:
    #         polygon_json = polygon.polygon_to_json()
    #         polygon_claims = polygon_json["properties"]['polygon_claims']
    #         polygon_json["properties"]['color'] = self.color_spot(
    #             polygon_claims, max_claims_value)\
    #             if polygon_claims else 'grey'
    #         data.append(polygon_json)
    #         for org in polygon.organizations.all():
    #             places.append({'data': org.id,
    #                            'value': org.name,
    #                            "centroid": polygon_json["properties"]['centroid'],
    #                            'org_type_id': org.org_type.type_id \
    #                            if org.org_type else 0})

    #     responce = {'data': data,
    #                 'places': places}

    #     if add:
    #         org_types = OrganizationType.objects.filter(
    #             type_id__in=list(set([x['org_type_id'] for x in places])))

    #         claim_type_sets = {}
    #         for org_type in org_types:
    #             claim_type_set = []
    #             for claim_type in org_type.claimtype_set.all():
    #                 claim_type_set.append({'id': claim_type.id,
    #                                       'value': claim_type.name})
    #             claim_type_sets[org_type.type_id] = claim_type_set

    #         # responce['claim_types'] = mark_safe(json.dumps(claim_type_sets))
    #         responce['claim_types'] = claim_type_sets
    #     return responce

    # def generate_brothers(self, add=False):
    #     brothers = self.layer.polygon_set.all()

    #     responce = {'data': [],
    #                 'places': []}
    #     if add:
    #         responce['claim_types'] = {}

    #     for brother in brothers:
    #         brother_childs = brother.generate_childs(add)
    #         if brother_childs:
    #             responce['data'].extend(brother_childs['data'])
    #             responce['places'].extend(brother_childs['places'])
    #             if add:
    #                 responce['claim_types'].update(brother_childs['claim_types'])
    #     return responce

    # def generate_layer(self, add=False):
    #     if self.level == self.district:
    #         responce = self.generate_brothers(add)
    #     else:
    #         responce = self.generate_childs(add)

    #     # pprint(responce)
    #     center = list(self.centroid.coords)
    #     center.reverse()
    #     geo_json = {
    #         'type': "FeatureCollection",
    #         'config': {
    #             'center': center,
    #             'zoom': self.zoom},
    #         'features': responce['data'],
    #     }
    #     # pprint(geo_json)

    #     layer = {'polygons': mark_safe(json.dumps(geo_json)),
    #              'places': mark_safe(json.dumps(responce['places'])),
    #              'layer_id': self.polygon_id}
    #     if add:
    #         layer['claim_types'] = mark_safe(json.dumps(responce['claim_types']))

    #     # pprint(layer)
    #     return layer
