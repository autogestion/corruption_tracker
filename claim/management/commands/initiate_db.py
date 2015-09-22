from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from claim.models import OrganizationType, Organization
from utils.common import read_map


class Command(BaseCommand):
    help = 'Fullfill database with basic data'

    def handle(self, *args, **options):
        for org_type in OrganizationType.ORG_TYPES:
            try:
                OrganizationType.objects.get(org_type=org_type[0])
            except OrganizationType.DoesNotExist:
                obj = OrganizationType(org_type=org_type[0])
                obj.save()
            except OrganizationType.MultipleObjectsReturned:
                pass

        map_data = read_map()
        for org in map_data['features']:
            try:
                Organization.objects.get(id=org['properties']['ID'])
            except Organization.DoesNotExist:

                if org['properties']['NAME'] is None:
                    org['properties']['NAME'] = _('No name')

                new_org = Organization(
                    id=org['properties']['ID'],
                    name=org['properties']['NAME'],
                    org_type=OrganizationType(id="0")
                )
                new_org.save()
