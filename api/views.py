from rest_framework import viewsets, filters

from claim.models import Claim, Organization
from api.serializers import ClaimSerializer,\
	OrganizationSerializer


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
