

from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.decorators import list_route

from claim.models import Claim, Organization,\
    OrganizationType
from geoinfo.models import Polygon

from api.serializers import ClaimSerializer,\
    OrganizationSerializer, OrganizationTypeSerializer
from api.permissions import CanPost, PostThrottle


class ClaimViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and creating Claims.

    - to get claims for organization, use .../claim/_org_id_
    Example:  .../claim/13/

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

    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    permission_classes = (CanPost,)
    throttle_classes = (PostThrottle,)

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created',)
    ordering = ('created',)

    def list(self, request):
        docs = {ind: x for ind, x in enumerate(self.__doc__.split('\n')) if x}
        return Response(docs)

    def retrieve(self, request, pk=None):

        queryset = Claim.objects.filter(organization__id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        # serializer = ClaimSerializer(queryset, many=True)
        # return Response(serializer.data)

    def perform_create(self, serializer):
        # print(self.request.data)
        user = None if self.request.user.is_anonymous() else self.request.user
        serializer.save(complainer=user)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and creating Organizations.

    - to get organizations for polygon, use .../organization/_polygon_id_
    Example:  .../organization/21citzhovt0002/

    - to search organizations by name, use .../organization/?search=_value_
    Example:  .../organization/?search=прок

    - to get list of organization types, use /organization/orgtypes/

    - to add organization use POST with next parameters:
    Example:
        'shape': '{'type': 'Polygon', 'coordinates': [ [ [ 36.296753463843954, 50.006170131432199 ], [ 36.296990304344928, 50.006113443092367 ], [ 36.296866409713009, 50.005899627208827 ], [ 36.296629569212049, 50.00595631580083 ], [ 36.296753463843954, 50.006170131432199 ] ] ]}', 
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
            docs = {ind: x for ind, x in enumerate(self.__doc__.split('\n')) if x}
            return Response(docs)

    def retrieve(self, request, pk=None):
        queryset = Organization.objects.filter(polygon__polygon_id=pk)
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # print(request.data)

        layer = Polygon.objects.get(
            polygon_id=request.data['layer_id'])

        polygon = Polygon(
            polygon_id=request.data['centroid'],
            centroid=geos.fromstr("POINT(%s %s)" % tuple(request.data['centroid'].split(','))),
            shape=request.data['shape'],
            address=request.data['address'],
            layer=layer,
            level=Polygon.building,
            zoom=17,
            is_verified=True)
        polygon.save()

        org_type = OrganizationType.objects.get(
            type_id=request.data['org_type'])

        organization = Organization(
            name=request.data['org_name'],
            org_type=org_type)
        organization.save()

        polygon.organizations.add(organization)
