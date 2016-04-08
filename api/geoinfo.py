
from django.contrib.gis import geos

from rest_framework.response import Response
from rest_framework import viewsets, mixins, filters

from geoinfo.models import Polygon

from api.serializers import PolygonSerializer,\
    PolygonNoShapeSerializer, extractor
from api.permissions import IsSafe


class PolygonViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint for obtaining poligons.

    - GET returns all polygons ordered by creation date

    .

    - to search polygons by addres, use .../polygon/?search=_value_

    Example:  .../polygon/?search=студ

    .
    
    - to get polygons, filtered by layer use .../polygon/_layer_/

    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4

    Example:  .../polygon/3/

    .
    """

    queryset = Polygon.objects.all().order_by('updated')
    serializer_class = PolygonNoShapeSerializer

    permission_classes = (IsSafe,)
    lookup_value_regex = '\d'
    lookup_field = 'layer'

    filter_backends = (filters.SearchFilter,)
    search_fields = ('address',)

    def retrieve(self, request, layer=4):

        queryset = self.queryset.filter(level=int(pk))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class GetNearestPolygons(viewsets.ViewSet):
    """
    API endpoint for getting polygons in radius (_distance_) to point (_coordinates_)

    - to get nearest polygons, use .../polygon/get_nearest/_layer_/_distance_/_coordinates_

    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4

    Example:  .../polygon/get_nearest/4/0.05/36.226147,49.986106/

    .
    
    - to search polygon by addres in nearest polygons, 
    use .../polygon/get_nearest/_layer_/_distance_/_coordinates_/?search=_value_

    Example:  .../polygon/get_nearest/4/0.05/36.226147,49.986106/?search=студ

    .
    """

    permission_classes = (IsSafe,)
    polygon = 'get_nearest'

    # def list(self, request):
    #     docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x}
    #     return Response(docs)

    def retrieve(self, request, layer, distance, coord):
        pnt = geos.fromstr("POINT(%s %s)" % tuple(coord.split(',')))
        queryset = Polygon.objects.filter(
            centroid__dwithin=(pnt, float(distance)), level=int(layer))

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(address__icontains=search)

        serializer = PolygonSerializer(queryset, many=True)
        return Response(serializer.data)


class FitBoundsPolygons(viewsets.ViewSet):
    """
    API endpoint for getting polygons that fit to bounds (_coordinates_ in W, S, E, N).

    - to get polygons, use .../polygon/fit_bounds/_layer_/_coordinates_

    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4

    Example:  .../polygon/fit_bounds/4/2.81,18.15,86.04,60.89/

    .
    
    - to search polygon by addres in polygons that fit bounds,
    use .../polygon/fit_bounds/_layer_/_coordinates_/?search=_value_

    Example:  .../polygon/fit_bounds/4/2.81,18.15,86.04,60.89/?search=студ

    .
    """

    permission_classes = (IsSafe,)
    polygon = 'fit_bounds'

    # def list(self, request):
    #     docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x}
    #     return Response(docs)

    def retrieve(self, request, layer, coord):

        raw = [x for x in coord.split(',')]
        area_coord = ((raw[0], raw[1]), (raw[0], raw[3]), (raw[2], raw[3]),
                      (raw[2], raw[1]), (raw[0], raw[1]))

        area_coord_str = ', '.join([' '.join(x) for x in area_coord])
        area = geos.GEOSGeometry('POLYGON ((%s))' % area_coord_str)

        queryset = Polygon.objects.filter(
            shape__within=area, level=int(layer))

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(address__icontains=search)

        serializer = PolygonSerializer(queryset, many=True)
        return Response(serializer.data)


class CheckInPolygon(viewsets.ViewSet):
    """
    API endpoint for check if coordinates in polygon.

    - to check in polygon, use  .../polygon/check_in/_layer_/_coordinates_

    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4

    Example:  .../polygon/check_in/4/36.2218621,49.9876059/
    .
    """

    permission_classes = (IsSafe,)
    polygon = 'check_in'

    # def list(self, request):
    #     docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x}
    #     return Response(docs)

    def retrieve(self, request, layer, coord):
        pnt = geos.fromstr("POINT(%s %s)" % tuple(coord.split(',')))
        queryset = Polygon.objects.filter(shape__contains=pnt, level=int(layer))

        serializer = PolygonSerializer(queryset, many=True)
        return Response(serializer.data)


class GetPolygonsTree(viewsets.ViewSet):
    """
    API endpoint for getting polygons ierarchy.

    - GET returns hole tree from 'root' polygon

    - to get tree from certain node, use .../polygon/get_tree/_polygon_id_

    Example:  .../polygon/get_tree/21citdzerz/

    .
    """

    permission_classes = (IsSafe,)
    lookup_field = 'polygon_id'

    def list(self, request):
        return Response(extractor('root'))

    def retrieve(self, request, polygon_id='root'):
        return Response(extractor(pk))
