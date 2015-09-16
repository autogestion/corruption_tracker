from django.contrib import admin

from claim.models import Claim


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('polygon_id', 'created', 'live', 'text')
    search_fields = ('polygon_id', 'text')
    list_filter = ('polygon_id', 'created')


admin.site.register(Claim, ClaimAdmin)
