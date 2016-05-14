# import json

from django.contrib.gis import admin
# from django import forms
# from django.conf import settings

from geoinfo.models import Uploader, Polygon
# from utils.geoparser import GeoJSONParser


# class UploaderForm(forms.ModelForm):
#     class Meta:
#         model = Uploader
#         fields = '__all__'

# class UploaderAdmin(admin.ModelAdmin):
#     form = UploaderForm


# class PolygonForm(forms.ModelForm):
#     class Meta:
#         model = Polygon
#         fields = '__all__'

#     def save(self, commit=True):
#         instance = super(PolygonForm, self).save(commit=False)
#         if instance.is_default:
#             try:
#                 default = Polygon.objects.get(is_default=True)

#                 if default != instance:
#                     default.is_default = False
#                     default.save()
#             except Polygon.DoesNotExist:
#                 pass

#         instance.save()
#         return instance

class PolygonAdmin(admin.OSMGeoAdmin):
    # form = PolygonForm
    list_display = ('polygon_id', 'layer',
                    'first_organization', 'address',
                    'total_claims',
                    # 'claims',
                    'centroid', 'level',
                    'zoom', 'is_verified',
                    'updated')
    search_fields = ('polygon_id', 'address')
    list_filter = ('level', 'is_verified', 'is_default')


# admin.site.register(Uploader, UploaderAdmin)
admin.site.register(Uploader)
admin.site.register(Polygon, PolygonAdmin)

