import json

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from claim.models import OrganizationType, Organization, Layer, Polygon
from utils.common import read_map


class Command(BaseCommand):
    help = 'Fullfill database with basic data'

    def handle(self, *args, **options):
        # Layers
        for layer_type in Layer.LAYER_TYPES:
            try:
                Layer.objects.get(layer_type=layer_type[0])
            except Layer.DoesNotExist:
                obj = Layer(layer_type=layer_type[0], name=layer_type[1])
                obj.save()
            except Layer.MultipleObjectsReturned:
                pass

        # Organization Types
        for org_type in OrganizationType.ORG_TYPES:
            try:
                OrganizationType.objects.get(org_type=org_type[0])
            except OrganizationType.DoesNotExist:
                obj = OrganizationType(org_type=org_type[0])
                obj.save()
            except OrganizationType.MultipleObjectsReturned:
                pass

        # Polygons n Orgs
        map_data = read_map()
        for org in map_data['features']:
            # Create polygon
            try:
                polygon = Polygon.objects.get(
                    polygon_id=org['properties']['ID'])
            except Polygon.DoesNotExist:
                polygon = Polygon(polygon_id=org['properties']['ID'],
                                  coordinates=json.dumps(org['geometry']),
                                  layer=Layer.objects.get(layer_type=0))
                polygon.save()

            # Create organization
            if org['properties']['NAME'] is None:
                org['properties']['NAME'] = _('No name')

            try:
                org_obj = Organization.objects.get(
                    name=org['properties']['NAME'])
            except Organization.DoesNotExist:
                org_obj = Organization(
                    name=org['properties']['NAME'],
                    org_type=OrganizationType.objects.get(org_type="0")
                )
                org_obj.save()

            # Link them
            polygon.organizations.add(org_obj)
