import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
# from django.contrib.gis.geos import fromstr


# from utils.common import get_geojson_file
from utils.geoparser import GeoJSONParser
from geoinfo.models import Polygon

class Command(BaseCommand):
    help = 'Fullfill database with basic data'

    def handle(self, *args, **options):

        call_command('loaddata', 'initial_data')

        geofilenames = os.listdir(settings.INIT_GEOJSON_FOLDER)
        fullpathes = [os.path.join(
                      settings.INIT_GEOJSON_FOLDER,
                      x) for x in geofilenames if x.endswith('.geojson')]
        geojsons = list(map(GeoJSONParser.get_geojson_file, fullpathes))
        geojsons.sort(key=lambda x: x['ctracker_config']['AL'])
        list(map(GeoJSONParser.geojson_to_db, geojsons))

        # try:
        #     default = Polygon.objects.get(polygon_id='21citzhovt')
        #     default.is_default = True
        #     default.centroid = fromstr("POINT(36.226147 49.986106)", srid=4326)
        #     default.save()
        # except Polygon.DoesNotExist:
        #     pass
