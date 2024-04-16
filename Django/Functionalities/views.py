import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FilmScrap
from dateutil.relativedelta import relativedelta as rd

@login_required
def recettes_page(request):
    return render(request, "functionalities/recettes_page.html")


@login_required
def predict_page(request):
    return render(request, "functionalities/prediction_page.html")


@login_required
def historique_page(request):
    return render(request, 'functionalities/historique_page.html')


@login_required
def nouveautes_page(request):
    films = FilmScrap.objects.order_by("classement")[:10]
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
