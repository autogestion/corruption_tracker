
import datetime

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from geoinfo.models import Polygon
from claim.models import Organization

from api.permissions import IsSafe, IsAuthenticatedOrCreate

from api.serializers import OrganizationSerializer, \
    PolygonNoShapeSerializer, SignUpSerializer

from django.contrib.auth.models import User
from rest_framework import generics

from oauth2_provider.models import Application


def get_test_app_client():
    try:
        test_app = Application.objects.get(name='test_app')
        return test_app.client_id
    except Application.DoesNotExist:
        return 'Application with name "test_app" have to be created'


class SignUp(mixins.CreateModelMixin, viewsets.GenericViewSet):
    __doc__ = """
    To authorize user make next steps:

    1) To create user, make POST .../sign_up/ call with username and password

    2) To get token, make POST .../token/ call with username, password, grant_type(='password') and client_id 

    Request must be x-www-form-urlencoded. Client_id for test requests: %s

    Client_id for real client must be created in admin, and set client type to "public" and grant type to "resource owner password based"

    3) To make an authenticated request, just pass the Authorization header in your requests. It's value will be "Bearer YOUR_ACCESS_TOKEN".

    .
    """ % get_test_app_client()


    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


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
    lookup_field = 'date'

    @detail_route()
    def polygon(self, request, date=None):
        start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        queryset = Polygon.objects.filter(updated__gte=start_date)
        serializer = PolygonNoShapeSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route()
    def organization(self, request, date=None):
        start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        queryset = Organization.objects.filter(updated__gte=start_date)
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)
