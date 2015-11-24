import json

from django.contrib.gis import admin
from django import forms
# Register your models here.
from geoinfo.models import Layer, Polygon
from utils.geoparser import GeoJSONParser


class LayerForm(forms.ModelForm):
    class Meta:
        model = Layer
        fields = '__all__'

    def save(self, commit=True):
        instance = super(LayerForm, self).save(commit=False)
        if instance.parse_file:
            geojson = json.loads(instance.json_file.read().decode('utf8'))
            return GeoJSONParser.geojson_to_db(geojson, return_instance=True)
        else:
            if commit:
                instance.save()
            return instance

    # def clean(self):
    #     if self.cleaned_data.get('parse_file') and\
    #        self.cleaned_data.get('json_file'):
    #         return self.cleaned_data
    #     else:
    #         super(LayerForm, self).clean()


class LayerAdmin(admin.ModelAdmin):
    form = LayerForm
    list_display = ('name', 'layer_type', 'is_default',
                    'zoom', 'center')
    search_fields = ('name',)
    list_filter = ('layer_type', 'zoom')


class PolygonAdmin(admin.OSMGeoAdmin):
    list_display = ('polygon_id', 'layer', 'organization_count', 'address')
    search_fields = ('polygon_id', 'address')
    list_filter = ('layer',)


admin.site.register(Layer, LayerAdmin)
admin.site.register(Polygon, PolygonAdmin)
