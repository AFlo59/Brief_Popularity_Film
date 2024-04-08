from django.db import models
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FilmScrap(models.Model):
    id = models.AutoField(primary_key=True)
    url_allo = models.URLField()
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    year_allo = models.SmallIntegerField(null=True)
    director_allo = models.JSONField(null=True)
    director_raw = models.JSONField(null=True)
    rating_press = models.FloatField(null=True)
    rating_public = models.FloatField(null=True)
    casting = models.JSONField(null=True)
    distributor = models.CharField(max_length=255, null=True)
    genre = models.JSONField(null=True)
    budget = models.BigIntegerField(null=True)
    lang = models.JSONField(null=True)
    visa = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    award = models.SmallIntegerField(null=True)
    thumbnail = models.URLField(null=True)


class Film(models.Model):
    titre = models.CharField(max_length=100)
    classement = models.IntegerField()
    portrait = models.URLField()
    duration = models.IntegerField()
    description = models.TextField()
    date_sortie = models.DateField()
    synopsis = models.TextField()
    genres = models.ManyToManyField("Genre", related_name="films")
    castings = models.ManyToManyField("Casting", related_name="films")
    countries = models.ManyToManyField("Country", related_name="films")

    def str(self):
        return self.titre


class Genre(models.Model):
    nom = models.CharField(max_length=100)

    def str(self):
        return self.nom


class Casting(models.Model):
    nom = models.CharField(max_length=100)

    def str(self):
        return self.nom


class Country(models.Model):
    nom = models.CharField(max_length=100)
