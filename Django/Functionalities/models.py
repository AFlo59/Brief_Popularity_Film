from django.db import models
from django.conf import settings
from django.utils import timezone

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class FilmScrap(models.Model):
    id = models.AutoField(primary_key=True)
    classement = models.IntegerField(null=True, blank=True)
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

# class HistoriqueManager(models.Manager):
#     def nettoyer_anciennes_donnees(self):
#         # Calculer la date limite pour conserver les données
#         date_limite = timezone.now().date() - timezone.timedelta(days=14)

#         # Supprimer les données plus anciennes que la date limite
#         self.filter(date_semaine__lt=date_limite).delete()

# class Historique(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date_semaine = models.DateField(default=timezone.now)

#     objects = HistoriqueManager()

#     def save(self, *args, **kwargs):
#         # Avant de sauvegarder l'objet Historique, nettoyer les anciennes données
#         Historique.objects.nettoyer_anciennes_donnees()
#         super().save(*args, **kwargs)


# class HistoriqueFilm(models.Model):
#     historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
#     film = models.ForeignKey('Film', on_delete=models.CASCADE)

# class HistoriqueRealisateur(models.Model):
#     historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
#     realisateur = models.ForeignKey('Realisateur', on_delete=models.CASCADE)

# class HistoriqueGenre(models.Model):
#     historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
#     genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

# class HistoriqueCasting(models.Model):
#     historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
#     casting = models.ForeignKey('Casting', on_delete=models.CASCADE)

# class HistoriqueCountry(models.Model):
#     historique = models.ForeignKey(Historique, on_delete=models.CASCADE)
#     country = models.ForeignKey('Country', on_delete=models.CASCADE)


