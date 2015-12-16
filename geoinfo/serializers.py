from rest_framework import serializers

from geoinfo.models import Layer, Polygon


class PolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon
        fields = ('organization_count')
