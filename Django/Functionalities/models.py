from django.db import models
from django.conf import settings
from django.utils import timezone

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class HistoriqueManager(models.Manager):
    def nettoyer_anciennes_donnees(self):
        # Calculer la date limite pour conserver les données
        date_limite = timezone.now().date() - timezone.timedelta(days=14)

        # Supprimer les données plus anciennes que la date limite
        self.filter(date_semaine__lt=date_limite).delete()

class Historique(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_semaine = models.DateField(default=timezone.now)

    objects = HistoriqueManager()

    def save(self, *args, **kwargs):
        # Avant de sauvegarder l'objet Historique, nettoyer les anciennes données
        Historique.objects.nettoyer_anciennes_donnees()
        super().save(*args, **kwargs)


class HistoriqueFilm(models.Model):
    historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
    film = models.ForeignKey('Film', on_delete=models.CASCADE)

class HistoriqueGenre(models.Model):
    historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

class HistoriqueCasting(models.Model):
    historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
    casting = models.ForeignKey('Casting', on_delete=models.CASCADE)

class HistoriqueCountry(models.Model):
    historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)


class Film(models.Model):
    titre = models.CharField(max_length=100)
    classement = models.IntegerField()
    portrait = models.URLField(null=True, blank=True) 
    duration = models.IntegerField()
    description = models.TextField()
    date_sortie = models.DateField()
    synopsis = models.TextField()
    genres = models.ManyToManyField('Genre', related_name='films')
    castings = models.ManyToManyField('Casting', related_name='films')
    countries = models.ManyToManyField('Country', related_name='films')

    def __str__(self):
        return self.titre


class Genre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Casting(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Country(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom