from django.contrib import admin

from claim.models import Claim, InCharge,\
    Organization, OrganizationType, ClaimType, Moderator


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'servant',
                    'claim_type', 'text', 'live',
                    'complainer', 'bribe', 'moderation', 'created')
    search_fields = ('organization', 'servant', 'text')
    list_filter = ('organization', 'created')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'org_type',
                    'first_polygon', 'claims', 'url',
                    'updated', 'is_verified')
    search_fields = ('name',)
    list_filter = ('org_type',)


class InChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')


class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name')
    search_fields = ('type_id', 'name')


class ClaimTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'linked_org_types')
    search_fields = ('name',)


admin.site.register(Claim, ClaimAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(InCharge, InChargeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(ClaimType, ClaimTypeAdmin)
admin.site.register(Moderator)
