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

    # def save(self, commit=True):
    #     # instance = super(UploaderForm, self).save(commit=False)
    #     geojson = json.loads(self.cleaned_data['json_file'].read().decode('utf8'))
    #     GeoJSONParser.geojson_to_db(geojson)
    #     # return instance


class UploaderAdmin(admin.ModelAdmin):
    form = UploaderForm
    # list_display = ('name', 'layer_type', 'is_default',
    #                 'zoom', 'center', 'higher')


class PolygonForm(forms.ModelForm):
    class Meta:
        model = Polygon
        fields = '__all__'

    def save(self, commit=True):
        instance = super(PolygonForm, self).save(commit=False)
        if instance.is_default:
            try:
                default = Polygon.objects.get(is_default=True)

                if default != instance:
                    default.is_default = False
                    default.save()
            except Polygon.DoesNotExist:
                pass

        instance.save()
        return instance


class PolygonAdmin(admin.OSMGeoAdmin):
    form = PolygonForm
    list_display = ('polygon_id', 'layer',
                    'first_organization', 'address', 'centroid',
                    'level', 'is_default', 'zoom')
    search_fields = ('polygon_id', 'address')
    list_filter = ('level', 'layer__polygon_id')


admin.site.register(Uploader, UploaderAdmin)
admin.site.register(Polygon, PolygonAdmin)
