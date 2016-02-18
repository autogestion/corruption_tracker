import json
import os, re
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import fromstr

from geoinfo.models import Polygon
from claim.models import OrganizationType, Organization, ClaimType


class GeoJSONParser():

    @staticmethod
    def get_geojson_file(file_path):
        # print(file_path)
        try:
            # python 3+
            json_s = open(file_path, encoding='utf8').read()
        except TypeError:
            # python 2
            json_s = open(file_path).read()
            json_s = json_s.decode('utf8')

        return json.loads(json_s)

    @staticmethod
    def geojson_to_db(geo_json, return_instance=False):
        centroidPattern = re.compile("(-?\d+(?:\.\d+)?)\D+(-?\d+(?:\.\d+)?)")

        if geo_json['ctracker_config']['AL'] == 4:
            try:
                default_claim_type = ClaimType.objects.get(name='---')
            except ClaimType.DoesNotExist:
                default_claim_type = ClaimType(name='---')
                default_claim_type.save()

                with open(os.path.join(settings.INIT_GEOJSON_FOLDER,
                          'habar.jpg'), 'rb') as x_logo:
                    xabar_file = File(x_logo)

                    xabar = ClaimType(name='Xabar', icon=xabar_file)
                    xabar.save()

        # Create polygons
        for feature in geo_json['features']:
            try:
                polygon = Polygon.objects.get(
                    polygon_id=feature['properties']['ID'])

            except Polygon.DoesNotExist:
                polygon = Polygon(
                    polygon_id=feature['properties']['ID'],
                    shape=json.dumps(feature['geometry']),
                    # centroid=GEOSGeometry('POINT(%s %s)') % (
                    #     feature['properties']['CENTROID'].split(',')),
                    centroid=fromstr("POINT(%s %s)" % centroidPattern.search(
                        feature['properties']['CENTROID']).groups(),
                        srid=4326),
                    address=feature['properties']['ADDRESS'],
                    level=geo_json['ctracker_config']['AL'],
                    zoom=geo_json['ctracker_config']['ZOOM'])

                if feature['properties']['PARENT']:
                    parent = Polygon.objects.get(
                        polygon_id=feature['properties']['PARENT'])
                    polygon.layer = parent

                polygon.save()

            if geo_json['ctracker_config']['AL'] == 4:
                org_names = feature['properties']['ORG_NAMES'].split('|')
                org_types = feature['properties']['ORG_TYPES'].split('|')
                for index, org_name in enumerate(org_names):
                    try:
                        org_obj = Organization.objects.get(
                            name=org_name)
                    except Organization.DoesNotExist:

                        try:
                            org_type = OrganizationType.objects.get(
                                type_id=org_types[index])
                        except OrganizationType.DoesNotExist:
                            org_type = OrganizationType(
                                type_id=org_types[index],
                                name=geo_json['ctracker_config']["ORG_TYPES"][org_types[index]])
                            org_type.save()
                            org_type.claimtype_set.add(
                                default_claim_type, xabar)

                        org_obj = Organization(
                            name=org_name,
                            org_type=org_type
                        )
                        org_obj.save()
                    except Organization.MultipleObjectsReturned:
                        pass

                    # Link them
                    polygon.organizations.add(org_obj)
