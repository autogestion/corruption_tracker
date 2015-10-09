import os

from django.core.management.base import BaseCommand
from django.conf import settings

# from claim.models import OrganizationType
from utils.common import get_geojson_file
from utils.geoparser import GeoJSONParser


class Command(BaseCommand):
    help = 'Fullfill database with basic data'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        # Organization Types, must be parsed from geojson
        # We don't use them any way

        # print('Creating organization types...')
        # for org_type in OrganizationType.ORG_TYPES:
        #     try:
        #         OrganizationType.objects.get(org_type=org_type[0])
        #     except OrganizationType.DoesNotExist:
        #         obj = OrganizationType(org_type=org_type[0])
        #         obj.save()
        #     except OrganizationType.MultipleObjectsReturned:
        #         pass

        # Polygons n Orgs
        if options['file']:
            geo_json = get_geojson_file(os.path.join(
                settings.INIT_GEOJSON_FOLDER, options['file']))
            GeoJSONParser.geojson_to_db(geo_json)
        else:
            for geo_json_file in os.listdir(settings.INIT_GEOJSON_FOLDER):
                geo_json = get_geojson_file(os.path.join(
                    settings.INIT_GEOJSON_FOLDER, geo_json_file))
                GeoJSONParser.geojson_to_db(geo_json)
