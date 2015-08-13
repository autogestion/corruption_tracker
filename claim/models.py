from django.db import models

class Claim(models.Model):
    text = models.CharField(max_length=2550)
    created = models.DateTimeField('auto_now_add=True')
    live = models.BooleanField()
