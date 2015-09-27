from django.contrib import admin

from claim.models import Claim, InCharge,\
    Organization, OrganizationType


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'servant',
                    'text', 'live', 'created')
    search_fields = ('organization', 'servant', 'text')
    list_filter = ('organization', 'created')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'org_type', 'total_claims')
    search_fields = ('name', 'org_type')
    list_filter = ('name', 'org_type')


class InChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')


admin.site.register(Claim, ClaimAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(InCharge, InChargeAdmin)
admin.site.register(OrganizationType)
