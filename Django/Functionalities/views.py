import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FilmScrap
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime, timedelta

@login_required
def recettes_page(request):
    return render(request, "functionalities/recettes_page.html")


@login_required
def predict_page(request):
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)
    films = FilmScrap.objects.filter(date__range=(today, one_week_later)).order_by("-score_pred")

    for film in films:
        if film.score_pred is not None:
            film.score_pred_divided = film.score_pred / 2000
        else:
            film.score_pred_divided = None

        if film.score_pred_divided is not None:
            film.score_pred_divided_divided = film.score_pred_divided / 7
        else:
            film.score_pred_divided_divided = None

        if film.score_pred_divided_divided is not None:
            film.recette_journaliere = min(film.score_pred_divided_divided * 10, 2000)
        else:
            film.recette_journaliere = None

        if film.recette_journaliere is not None:
             film.recette_hebdomadaire = film.recette_journaliere * 7
        else:
             film.recette_hebdomadaire = None
        
        if film.recette_hebdomadaire is not None:
            film.benefice_hebdomadaire = film.recette_hebdomadaire - 4900
        else:
            film.benefice_hebdomadaire = None
    
    return render(request, "functionalities/prediction_page.html", {"films": films})


@login_required
def historique_page(request):
    return render(request, 'functionalities/historique_page.html')



@login_required
def nouveautes_page(request):
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)
    films = FilmScrap.objects.filter(date__range=(today, one_week_later)).order_by("classement")[:10]
    fmt = '{0.hours}h {0.minutes}'
    for film in films:
        if film.duration is not None:
            film.duration = fmt.format(rd(seconds=film.duration))
        if isinstance(film.genre, list):
            film.genre = ', '.join(film.genre)
        if isinstance(film.casting, list):
            film.casting = ', '.join(film.casting)
        if isinstance(film.director, list):
            film.director = ', '.join(film.director)
    return render(request, "functionalities/nouveautes_page.html", {"films": films})
