import json

from django.conf import settings
from django.core.management.base import BaseCommand
# from django.utils.translation import ugettext as _

from claim.models import OrganizationType, Organization
from geoinfo.models import Layer, Polygon
from utils.common import get_geojson_file


class Command(BaseCommand):
    help = 'Fullfill database with basic data'

    def handle(self, *args, **options):
        # TODO(autogestion) This command have to
        # accept additional argument - filename of GeoJSON.
        # Files could be stored in separate folder where command
        # will look for recived filename.
        # This GeoJSON would contain Layer name and type,
        # and all of the polygons inside file will be linked
        # to this Layer
        # Without addional argument command should parse all
        # files it that folder

        # Layers
        # Temporary hack, before Layer appear in GeoJSON
        try:
            layer = Layer.objects.get(layer_type=Layer.ORGANIZATION,
                                      name=settings.DEFAULT_LAYER_NAME)
        except Layer.DoesNotExist:
            layer = Layer(layer_type=Layer.ORGANIZATION,
                          name=settings.DEFAULT_LAYER_NAME, is_default=True)
            layer.save()

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
        map_data = get_geojson_file()
        for org in map_data['features']:

            # Create polygon
            try:
                polygon = Polygon.objects.get(
                    polygon_id=org['properties']['ID'])

                # Temporary hack, before Layer appear in GeoJSON
                if polygon.layer.name != 'Kharkiv_Test':
                    polygon.layer = layer
                    polygon.save()

                # Temporary hack to kill off organizations without names
                if not org['properties']['NAME']:
                    for emtpy_org in polygon.organizations.all():
                        emtpy_org.delete()
                    polygon.delete()
                    continue

            except Polygon.DoesNotExist:
                # Hack to avoid organizations without names
                if not org['properties']['NAME']:
                    continue

                polygon = Polygon(polygon_id=org['properties']['ID'],
                                  coordinates=json.dumps(org['geometry']),
                                  layer=layer)
                polygon.save()

            # Create organization
            # Temporary, fix unknown organization type
            org_type = OrganizationType.objects.get(org_type="0")

            try:
                org_obj = Organization.objects.get(
                    name=org['properties']['NAME'])
            except Organization.DoesNotExist:
                org_obj = Organization(
                    name=org['properties']['NAME'],
                    org_type=org_type
                )
                org_obj.save()
            except Organization.MultipleObjectsReturned:
                # Temporary fix to avoid organizations without types
                orgs = Organization.objects.filter(
                    name=org['properties']['NAME'])
                for org in orgs:
                    org.org_type = org_type
                    org.save()

            # Temporary fix of found error:
            try:
                org_obj.org_type
            except OrganizationType.DoesNotExist:
                org_obj.org_type = org_type
                org_obj.save()

            # Link them
            polygon.organizations.add(org_obj)

        # Temporary, delete No name organizations
        no_name = Organization.objects.filter(name='No name')
        for no_name_org in no_name:
            no_name_org.delete()

        # Temporary, to add additional organizations
        # to north terminal
        org_type = OrganizationType.objects.get(org_type="0")
        north_terminal = Polygon.objects.get(polygon_id='1296')
        if north_terminal.organizations.all().count() < 3:
            for new_org in ['Довідкова', 'Каси']:
                new_org_obj = Organization(
                    name=new_org,
                    org_type=org_type
                )
                new_org_obj.save()
                north_terminal.organizations.add(new_org_obj)
