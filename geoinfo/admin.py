import json

from django.contrib.gis import admin
from django import forms
# Register your models here.
from geoinfo.models import Uploader, Polygon
from utils.geoparser import GeoJSONParser


class UploaderForm(forms.ModelForm):
    class Meta:
        model = Uploader
        fields = '__all__'

    def save(self, commit=True):
        instance = super(UploaderForm, self).save(commit=commit)
        geojson = json.loads(instance.json_file.read().decode('utf8'))
        GeoJSONParser.geojson_to_db(geojson)
        return instance


class UploaderAdmin(admin.ModelAdmin):
    form = UploaderForm
    # list_display = ('name', 'layer_type', 'is_default',
    #                 'zoom', 'center', 'higher')


class PolygonAdmin(admin.OSMGeoAdmin):
    list_display = ('polygon_id', 'layer', 'organization_count',
                    'address', 'centroid', 'level', 'is_default',
                    'zoom')
    search_fields = ('polygon_id', 'address')
    list_filter = ('level', 'layer__polygon_id')


admin.site.register(Uploader, UploaderAdmin)
admin.site.register(Polygon, PolygonAdmin)
