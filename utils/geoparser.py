import json

from geoinfo.models import Layer, Polygon
from claim.models import OrganizationType, Organization


class GeoJSONParser():

    @staticmethod
    def geojson_to_db(geo_json):
        layer_info = geo_json['ctracker_config']
        print('Processing %s geojson...' % layer_info['layer_name'])
        try:
            layer = Layer.objects.get(name=layer_info['layer_name'])
        except Layer.DoesNotExist:
            layer = Layer(
                layer_type=getattr(Layer, layer_info['layer_type']),
                name=layer_info['layer_name'],
                is_default=bool(layer_info['set_default']))
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

                polygon = Polygon(polygon_id=feature['properties']['ID'],
                                  coordinates=json.dumps(feature['geometry']),
                                  layer=layer)
                polygon.save()

            # Create organization
            # Temporary, fix unknown organization type
            org_type = OrganizationType.objects.get(org_type="0")

            try:
                org_obj = Organization.objects.get(
                    name=feature['properties']['NAME'])
            except Organization.DoesNotExist:
                org_obj = Organization(
                    name=feature['properties']['NAME'],
                    org_type=org_type
                )
                org_obj.save()
            except Organization.MultipleObjectsReturned:
                pass

            # Link them
            polygon.organizations.add(org_obj)

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
