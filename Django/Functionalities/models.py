from django.db import models
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Film(models.Model):
    titre = models.CharField()
    classement = models.IntegerField()
    portrait = models.URLField() 
    duration = models.IntegerField()
    description = models.TextField()
    date_sortie = models.DateField()
    synopsis = models.TextField()
    genres = models.ManyToManyField('Genre', related_name='films')
    castings = models.ManyToManyField('Casting', related_name='films')
    countries = models.ManyToManyField('Country', related_name='films')

    def str(self):
        return self.titre

class Genre(models.Model):
    nom = models.CharField()

    def str(self):
        return self.nom

class Casting(models.Model):
    nom = models.CharField()

    def str(self):
        return self.nom

class Country(models.Model):
    nom = models.CharField()