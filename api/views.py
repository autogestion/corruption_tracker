
import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from geoinfo.models import Polygon
from claim.models import Organization

from api.permissions import IsSafe

from api.serializers import OrganizationSerializer, \
    PolygonNoShapeSerializer


class GetUpdatedViewSet(viewsets.ViewSet):
    """
    API endpoint for getting new added organizations and poligons.

    - to get organizations, created or updated after certain date,
    use  .../updated/_date_/organization/
    Example:  .../update/2016-03-01/organization/

    - to get polygons, created or updated after certain date,
    use  .../updated/_date_/polygon/
    Example:  .../update/2016-03-01/polygon/

    date must be in ISO format

    .
    """

    permission_classes = (IsSafe,)
    lookup_value_regex = '\d{4}-\d{2}-\d{2}'

    def list(self, request):
        docs = {ind: x for ind, x in enumerate(self.__doc__.split('\n')) if x}
        return Response(docs)

    @detail_route()
    def polygon(self, request, pk=None):
        start_date = datetime.datetime.strptime(pk, '%Y-%m-%d')
        queryset = Polygon.objects.filter(updated__gte=start_date)
        serializer = PolygonNoShapeSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route()
    def organization(self, request, pk=None):
        start_date = datetime.datetime.strptime(pk, '%Y-%m-%d')
        queryset = Organization.objects.filter(updated__gte=start_date)
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)
