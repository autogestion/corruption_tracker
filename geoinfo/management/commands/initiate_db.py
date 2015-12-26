import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from utils.common import get_geojson_file
from utils.geoparser import GeoJSONParser


class Command(BaseCommand):
    help = 'Fullfill database with basic data'

    # def add_arguments(self, parser):
    #     parser.add_argument('--file', type=str)

    def handle(self, *args, **options):

        # Polygons n Orgs
        # if options['file']:
        #     geo_json = get_geojson_file(os.path.join(
        #         settings.INIT_GEOJSON_FOLDER, options['file']))
        #     GeoJSONParser.geojson_to_db(geo_json)
        # else:

        call_command('loaddata', 'initial_data')

        geofilenames = os.listdir(settings.INIT_GEOJSON_FOLDER)
        fullpathes = [os.path.join(
                      settings.INIT_GEOJSON_FOLDER, x) for x in geofilenames]
        geojsons = list(map(get_geojson_file, fullpathes))
        geojsons.sort(key=lambda x: x['ctracker_config']['AL'])
        list(map(GeoJSONParser.geojson_to_db, geojsons))

        # for geo_json_file in os.listdir(settings.INIT_GEOJSON_FOLDER):
        #     geo_json = get_geojson_file(os.path.join(
        #         settings.INIT_GEOJSON_FOLDER, geo_json_file))
        #     GeoJSONParser.geojson_to_db(geo_json)
