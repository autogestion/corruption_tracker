import datetime
from django.db import models

class Claim(models.Model):
    text = models.CharField(max_length=2550)
    created = models.DateTimeField(default=datetime.datetime.now)
    live = models.BooleanField(default=False)
    polygon_id = models.CharField(max_length=250)
