from django.contrib import admin

from claim.models import Claim, Organization, InCharge,\
    OrganizationType, Layer, Polygon


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('polygon_id', 'organization', 'servant',
        'text', 'live', 'created')
    search_fields = ('polygon_id', 'text')
    list_filter = ('polygon_id', 'created')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'org_type')
    search_fields = ('name', 'org_type')
    list_filter = ('name', 'org_type')


class InChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')


class PolygonAdmin(admin.ModelAdmin):
    list_display = ('polygon_id', 'layer')
    search_fields = ('olygon_id',)
    list_filter = ('layer',)


admin.site.register(Claim, ClaimAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(InCharge, InChargeAdmin)
admin.site.register(OrganizationType)
admin.site.register(Layer)
admin.site.register(Polygon, PolygonAdmin)
