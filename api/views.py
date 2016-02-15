from rest_framework import viewsets, filters

from claim.models import Claim, Organization,\
	ClaimType
from api.serializers import ClaimSerializer,\
	OrganizationSerializer, ClaimTypeSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating claims."""

    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_fields = ('organization__id', )

    ordering_fields = ('created', )


class OrganizationViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating claims."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    filter_backends = (
        filters.DjangoFilterBackend,  
    )
    filter_fields = ('polygon__polygon_id', )



class ClaimTypeViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating claims."""

    queryset = ClaimType.objects.all()
    serializer_class = ClaimTypeSerializer

    filter_backends = (
        filters.DjangoFilterBackend,  
    )
    filter_fields = ('org_type__type_id', )


