
from rest_framework import viewsets, filters
from claim.models import Claim
from api.serializers import ClaimSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating claims."""

    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    filter_backends = (
        # filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    ordering_fields = ('created', )
