from django.contrib import admin

# Register your models here.
from geoinfo.models import Layer, Polygon


class PolygonAdmin(admin.ModelAdmin):
    list_display = ('polygon_id', 'layer', 'organization_count')
    search_fields = ('olygon_id',)
    list_filter = ('layer',)


admin.site.register(Layer)
admin.site.register(Polygon, PolygonAdmin)
