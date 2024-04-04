# Generated by Django 4.2.11 on 2024-04-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Genre',
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
                ('portrait', models.URLField()),
                ('duration', models.IntegerField()),
                ('description', models.TextField()),
                ('date_sortie', models.DateField()),
                ('synopsis', models.TextField()),
                ('castings', models.ManyToManyField(related_name='films', to='Functionalities.casting')),
                ('countries', models.ManyToManyField(related_name='films', to='Functionalities.country')),
                ('genres', models.ManyToManyField(related_name='films', to='Functionalities.genre')),
            ],
        ),
    ]
