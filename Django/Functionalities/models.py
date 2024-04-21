import json
import json
from django.db import models
from django.conf import settings
from django.utils import timezone

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FilmScrap(models.Model):
    id = models.AutoField(primary_key=True)
    classement = models.IntegerField(null=True, blank=True)
    score_pred = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True)
    score_pred = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField(null=True)
    director = models.JSONField(max_length=255, null=True)
    rating_press = models.FloatField(null=True)
    rating_public = models.FloatField(null=True)
    casting = models.JSONField(max_length=255, null=True)
    distributor = models.CharField(max_length=255, null=True)
    genre = models.JSONField(max_length=255, null=True)
    budget = models.BigIntegerField(null=True)
    lang = models.CharField(max_length=255, null=True)
    copies = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True)
    award = models.SmallIntegerField(null=True)
    thumbnail = models.URLField(null=True)
    score_pred = models.IntegerField(null=True, blank=True)
