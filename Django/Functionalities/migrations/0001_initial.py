# Generated by Django 4.2.11 on 2024-04-08 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Casting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('classement', models.IntegerField()),
                ('portrait', models.URLField(blank=True, null=True)),
                ('duration', models.IntegerField()),
                ('description', models.TextField()),
                ('date_sortie', models.DateField()),
                ('synopsis', models.TextField()),
                ('castings', models.ManyToManyField(related_name='films', to='Functionalities.casting')),
                ('countries', models.ManyToManyField(related_name='films', to='Functionalities.country')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_semaine', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Realisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueRealisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('historique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.historique')),
                ('realisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.realisateur')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.genre')),
                ('historique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.historique')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueFilm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.film')),
                ('historique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.historique')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.country')),
                ('historique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.historique')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueCasting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.casting')),
                ('historique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Functionalities.historique')),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(related_name='films', to='Functionalities.genre'),
        ),
        migrations.AddField(
            model_name='film',
            name='realisateurs',
            field=models.ManyToManyField(related_name='films', to='Functionalities.realisateur'),
        ),
    ]