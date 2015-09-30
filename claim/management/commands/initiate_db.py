
from django.core.management.base import BaseCommand
# from django.utils.translation import ugettext as _

from claim.models import OrganizationType

from utils.common import get_geojson_file
from utils.geoparser import GeoJSONParser


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
        geo_json = get_geojson_file()
        GeoJSONParser.geojson_to_db(geo_json)
