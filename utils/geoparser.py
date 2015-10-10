import json

from geoinfo.models import Layer, Polygon
from claim.models import OrganizationType, Organization


class GeoJSONParser():

    @staticmethod
    def geojson_to_db(geo_json):
        layer_info = geo_json['ctracker_config']

        global_org_type = False
        if 'global_org_type' in layer_info:
            try:
                global_org_type = OrganizationType.objects.get(
                    type_id=layer_info['global_org_type'])
            except OrganizationType.DoesNotExist:
                global_org_type = OrganizationType(
                    type_id=layer_info['global_org_type'],
                    name=layer_info['global_org_type_name'])
                global_org_type.save()

        print('Processing %s geojson...' % layer_info['layer_name'])
        try:
            layer = Layer.objects.get(name=layer_info['layer_name'])
        except Layer.DoesNotExist:
            layer = Layer(
                layer_type=getattr(Layer, layer_info['layer_type']),
                name=layer_info['layer_name'],
                is_default=bool(layer_info['set_default']),
                zoom=layer_info['zoom'],
                center=json.dumps(layer_info['center']))
            layer.save()

        for feature in geo_json['features']:
            # Create polygon
            try:
                polygon = Polygon.objects.get(
                    polygon_id=feature['properties']['ID'])
            except Polygon.DoesNotExist:
                # Hack to avoid organizations without names
                if not feature['properties']['NAME']:
                    continue

                polygon = Polygon(
                    polygon_id=feature['properties']['ID'],
                    shape=json.dumps(feature['geometry']),
                    centroid=json.dumps([
                        feature['properties']["CEN_LAT"],
                        feature['properties']["CEN_LONG"]]),
                    layer=layer)
                polygon.save()

            # Create organization
            # Temporary, fix unknown organization type
            org_type = global_org_type

            polygon_orgs = feature['properties']['NAME'].split('|')
            for org_name in polygon_orgs:
                try:
                    org_obj = Organization.objects.get(
                        name=org_name)
                except Organization.DoesNotExist:
                    org_obj = Organization(
                        name=org_name,
                        org_type=org_type
                    )
                    org_obj.save()
                except Organization.MultipleObjectsReturned:
                    pass

                # Link them
                polygon.organizations.add(org_obj)
