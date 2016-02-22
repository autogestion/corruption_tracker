import json

from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import fromstr
from rest_framework import viewsets, filters
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response

from geoinfo.models import Polygon
from claim.models import Claim, Organization,\
    ClaimType
from api.serializers import ClaimSerializer,\
    OrganizationSerializer, ClaimTypeSerializer, extractor


class IsSafe(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True


class CanPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS + ('POST',):
            return True

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS + ('POST',):
            return True


class ClaimViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and creating Claims.
    - to add claim use POST request
    - to get claims for organization, use .../claims/_org_id_
    Example:  .../claims/13/
    """

    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (CanPost,)

    filter_backends = (
        filters.OrderingFilter,
    )
    ordering_fields = ('created', )

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk=None):
        queryset = Claim.objects.filter(organization__id=pk)   
        serializer = ClaimSerializer(queryset, many=True)
        return Response(serializer.data)        


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing Organizations.
    - to get organizations for polygon, use .../organizations/_polygon_id_
    Example:  .../organizations/21citzhovt0002/
    """

    queryset = Organization.objects.all()
    permission_classes = (IsSafe,)

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk=None):
        queryset = Organization.objects.filter(polygon__polygon_id=pk)   
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)



class ClaimTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing ClaimTypes.
    - to get claim types for organization type, use .../claim_types/_org_type_id_
    Example:  .../claim_types/CNAP/
    """

    queryset = ClaimType.objects.all()
    permission_classes = (IsSafe,)

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk=None):
        queryset = ClaimType.objects.filter(org_type__type_id=pk)   
        serializer = ClaimTypeSerializer(queryset, many=True)
        return Response(serializer.data)



class GetPolygonsTree(viewsets.ViewSet):
    """
    API endpoint for getting polygons ierarchy.
    - GET returns hole tree from 'root' polygon
    - to get tree from certain node, use .../get_polygons_tree/_polygon_id_
    Example:  .../get_polygons_tree/21citdzerz/
    """

    def list(self, request):
        return Response(extractor('root'))

    def retrieve(self, request, pk='root'):     
        return Response(extractor(pk))

    queryset = Polygon.objects.all()
    permission_classes = (IsSafe,)


class GetNearestPolygons(viewsets.ViewSet):
    """
    API endpoint for getting nearest polygons.  
    - to get nearest polygons, use .../get_nearest_polygons/_layer_distance_lat_lang_
    Example:  .../get_nearest_polygons/4_0,05_36,226147_49,986106/
    """

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk=None):
        layer, distance, lat, lang = tuple(pk.split('_'))
        pnt = fromstr("POINT(%s %s)" % (lat.replace(',', '.'), lang.replace(',', '.')))
        selected = Polygon.objects.filter(
            centroid__dwithin=(pnt, float(distance.replace(',', '.'))), level=int(layer))

        data = [x.polygon_to_json() for x in selected]
        return Response(data)

    queryset = Polygon.objects.all()
    permission_classes = (IsSafe,)


class CheckInPolygon(viewsets.ViewSet):
    """
    API endpoint for check in polygon.  
    - to check in polygon, use .../check_in_polygon/_layer_lat_lang_
    Example:  .../check_in_polygon/4_36,2218621_49,9876059/
    """

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk='root'):   
        layer, lat, lang = tuple(pk.split('_'))  
        pnt = fromstr("POINT(%s %s)" % (lat.replace(',', '.'), lang.replace(',', '.')))
        selected = Polygon.objects.filter(shape__contains=pnt, level=int(layer))

        data = [x.polygon_to_json() for x in selected]
        return Response(data)

    queryset = Polygon.objects.all()
    permission_classes = (IsSafe,)

