from django.db import models


class URL(models.Model):
    url = models.URLField(max_length=200)
    slug = models.CharField(max_length=15)
    hit_counter = models.IntegerField(default=0, blank=True)
