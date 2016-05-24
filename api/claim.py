from django.contrib.gis import geos

from rest_framework.response import Response
from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import list_route, detail_route

from claim.models import Claim, Organization,\
    OrganizationType
from geoinfo.models import Polygon

from api.serializers import ClaimSerializer,\
    OrganizationSerializer, OrganizationTypeSerializer
from api.permissions import CanPost, PostThrottle


class ClaimViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint for listing and creating Claims.

    - to get claims for organization, use .../claim/_id_

    Example:  .../claim/13/

    .

    - to get claims for user, use .../claim/_id_/user/

    Example:  .../claim/2/user/

    .


    - to add claim use POST request with next parameters:
        'text', 'live', 'organization', 'servant', 'claim_type',

    Example:
        'text': 'Покусали комарі',
        'claim_type': '2',
        'servant': 'Бабця',
        'live': 'true',
        'organization': '13',
        'bribe': '50'
    .
    """

    queryset = Claim.objects.all().order_by('-created')
    serializer_class = ClaimSerializer

    permission_classes = (CanPost,)
    throttle_classes = (PostThrottle,)
    lookup_field = 'id'

    @detail_route()
    def user(self, request, id=None):
        queryset = self.queryset.filter(complainer__id=id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = self.queryset.filter(organization__id=id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        print(self.request.user)
        print(self.request.POST)
        user = None if self.request.user.is_anonymous() else self.request.user
        serializer.save(complainer=user)


class OrganizationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    API endpoint for listing and creating Organizations.

    - to get organizations for polygon, use .../organization/_polygon_id_

    Example:  .../organization/21citzhovt0002/

    .

    - to search organizations by name, use .../organization/?search=_value_

    Example:  .../organization/?search=прок

    .

    - to get list of organization types, use /organization/orgtypes/

    .

    - to add organization use POST with next parameters:
    
    Example:
        'shape': '{'type': 'Polygon', 'coordinates': [ [ [ 36.296753463843954,
            50.006170131432199 ], [ 36.296990304344928, 50.006113443092367 ],
            [ 36.296866409713009, 50.005899627208827 ], [ 36.296629569212049,
            50.00595631580083 ], [ 36.296753463843954, 50.006170131432199 ] ] ]}',
        'org_type': 'prosecutors',
        'layer_id': '21citzhovt',
        'address': 'Shevshenko street, 3',
        'org_name': 'Ministry of defence',
        'centroid': '36.2968099,50.0060348'

    .
    """


    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    permission_classes = (CanPost,)
    throttle_classes = (PostThrottle,)
    lookup_field = 'polygon_id'

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @list_route()
    def orgtypes(self, request):
        org_types = OrganizationType.objects.all()
        serializer = OrganizationTypeSerializer(org_types, many=True)
        return Response(serializer.data)

    def list(self, request):
        search = self.request.query_params.get('search', None)
        if search:
            return super(OrganizationViewSet, self).list(request)
        else:
            return Response('can be used only with ?search=')

    def retrieve(self, request, polygon_id=None):
        queryset = Organization.objects.filter(polygon__polygon_id=polygon_id)
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        parent_polygon_id = request.data.get('parent_polygon_id', None)
        polygon_id = request.data.get('polygon_id', None)
        level = request.data.get('level', None)
        centroid = request.data['centroid']
        centroid_pnt = geos.fromstr("POINT(%s %s)" % tuple(centroid.split(',')))

        layer = None
        if parent_polygon_id:
            layer = Polygon.objects.get(polygon_id=parent_polygon_id)
        else:
            districts = Polygon.objects.filter(shape__contains=centroid_pnt,
                                               level=Polygon.district)
            if districts:
                layer = districts[0]

        if not polygon_id:
            polygon_id = centroid

        if not level:
            level = Polygon.building

        polygon = Polygon(
            polygon_id=polygon_id,
            centroid=centroid_pnt,
            shape=request.data.get('shape', None),
            address=request.data['address'],
            layer=layer,
            level=level,
            is_verified=False)
        polygon.save()

        org_type = OrganizationType.objects.get(
            type_id=request.data['org_type'])

        organization = Organization(
            name=request.data['name'],
            org_type=org_type,
            is_verified=False)
        organization.save()

        polygon.organizations.add(organization)

        serializer = self.get_serializer(organization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
