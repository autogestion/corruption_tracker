import json

from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import fromstr
from rest_framework import viewsets, filters
from rest_framework.permissions import BasePermission, SAFE_METHODS

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


class ClaimViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating claims."""

    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (CanPost,)

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
    permission_classes = (IsSafe,)

    filter_backends = (
        filters.DjangoFilterBackend,
    )
    filter_fields = ('polygon__polygon_id', )


class ClaimTypeViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating claims."""

    queryset = ClaimType.objects.all()
    serializer_class = ClaimTypeSerializer
    permission_classes = (IsSafe,)

    filter_backends = (
        filters.DjangoFilterBackend,
    )
    filter_fields = ('org_type__type_id', )


def get_polygons_tree(request, polygon_id):
    data = mark_safe(json.dumps(extractor(polygon_id)))
    return HttpResponse(data, content_type='application/json')


def get_nearest_polygons(request, layer, distance, coord):
    pnt = fromstr("POINT(%s %s)" % tuple(coord.split(',')))
    selected = Polygon.objects.filter(
        centroid__dwithin=(pnt, float(distance)), level=int(layer))

    data = mark_safe(json.dumps([x.polygon_to_json() for x in selected]))
    return HttpResponse(data, content_type='application/json')


def check_in_building(request, layer, coord):
    pnt = fromstr("POINT(%s %s)" % tuple(coord.split(',')))

    selected = Polygon.objects.filter(shape__contains=pnt, level=int(layer))

    data = mark_safe(json.dumps([x.polygon_to_json() for x in selected]))
    return HttpResponse(data, content_type='application/json')
