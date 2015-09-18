import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count


class Claim(models.Model):
    text = models.CharField(max_length=2550)
    created = models.DateTimeField(default=datetime.datetime.now)
    live = models.BooleanField(default=False)
    polygon_id = models.CharField(max_length=250)
    servant = models.CharField(max_length=550)
    complainer = models.ForeignKey(User, null=True, blank=True, default=None)

    @classmethod
    def update_map(cls, json_data):
        """
        Update map with cliam information
        """
        polygons_values = cls.objects.values('polygon_id').\
            annotate(count=Count('polygon_id'))

        polygons_dict = {}
        for values_dict in polygons_values:
            polygons_dict[values_dict['polygon_id']] = values_dict['count']

        for polygon in json_data["features"]:
            polygon['claim_count'] = polygons_dict.get(
                str(polygon["properties"]["ID"]), 0)
