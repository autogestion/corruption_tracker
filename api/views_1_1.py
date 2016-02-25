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


class OnlyPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('POST',):
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
    .
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

    def perform_create(self, serializer):
        print(self.request.user)
        user = None if self.request.user.is_anonymous() else self.request.user
        serializer.save(complainer=user)



class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing Organizations.
    - to get organizations for polygon, use .../organizations/_polygon_id_
    
    Example:  .../organizations/21citzhovt0002/
    .
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
    .
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
    .
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
    .
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
    .
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



class AddOrganization(viewsets.ViewSet):
    """
    API endpoint for adding organization with polygon.  
    - use POST with next parameters:

    Example:
        'shape': '{'type': 'Polygon', 'coordinates': [ [ [ 36.296753463843954, 50.006170131432199 ], [ 36.296990304344928, 50.006113443092367 ], [ 36.296866409713009, 50.005899627208827 ], [ 36.296629569212049, 50.00595631580083 ], [ 36.296753463843954, 50.006170131432199 ] ] ]}', 
        'org_type': 'prosecutors',
        'layer_id': '21citzhovt',
        'address': 'Shevshenko street, 3',
        'org_name': 'Ministry of defence',
        'centroid': '36.2968099,50.0060348'
    .
    """

    def create(self, request):
        print(request.POST)

        layer = Polygon.objects.get(
            polygon_id=request.POST['layer_id'])

        polygon = Polygon(
            polygon_id=request.POST['centroid'],
            centroid=fromstr("POINT(%s %s)" % tuple(request.POST['centroid'].split(','))),
            shape=request.POST['shape'],
            address=request.POST['address'],
            layer=layer,
            level=Polygon.building,
            zoom=17,
            is_verified=True)
        polygon.save()

        org_type = OrganizationType.objects.get(
            type_id=request.POST['org_type'])

        organization = Organization(
            name=request.POST['org_name'],
            org_type=org_type)
        organization.save()

        polygon.organizations.add(organization)

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)


    queryset = Polygon.objects.all()
    permission_classes = (OnlyPost,)