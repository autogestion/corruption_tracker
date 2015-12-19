import json

from geoinfo.models import Polygon
from claim.models import OrganizationType, Organization


class GeoJSONParser():

    @staticmethod
    def geojson_to_db(geo_json, return_instance=False):

        # Create polygons
        for feature in geo_json['features']:
            try:
                polygon = Polygon.objects.get(
                    polygon_id=feature['properties']['ID'])

            except Polygon.DoesNotExist:
                polygon = Polygon(
                    polygon_id=feature['properties']['ID'],
                    shape=json.dumps(feature['geometry']),
                    centroid=feature['properties']['CENTROID'],
                    address=feature['properties']['ADDRESS'],
                    level=geo_json['ctracker_config']['AL'],
                    zoom=geo_json['ctracker_config']['ZOOM'])

                if feature['properties']['PARENT']:
                    parent = Polygon.objects.get(
                        polygon_id=feature['properties']['PARENT'])
                    polygon.layer = parent

                polygon.save()

            if feature['properties']['ORG_NAMES']:
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
                            org_type = OrganizationType(type_id=org_types[index],
                                                        name='Temp name')
                            org_type.save()

                        org_obj = Organization(
                            name=org_name,
                            org_type=org_type
                        )
                        org_obj.save()
                    except Organization.MultipleObjectsReturned:
                        pass

                    # Link them
                    polygon.organizations.add(org_obj)
