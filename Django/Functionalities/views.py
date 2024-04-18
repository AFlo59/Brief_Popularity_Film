import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FilmScrap
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse

def capitalize_name(name):
    if name:
        return ' '.join([part.capitalize() for part in name.split(' ')])
    return None

def recettes_page(request):
    today = datetime.now().date()
    current_weekday = today.weekday()

    days_until_wednesday = (2 - current_weekday) % 7
    wednesday_this_week = today + timedelta(days=days_until_wednesday)
    next_tuesday = wednesday_this_week + timedelta(days=6)

    films = FilmScrap.objects.filter(date__gte=wednesday_this_week, date__lte=next_tuesday).order_by("-score_pred").values('title', 'id', 'score_pred')

    # Exemples de limites de capacité pour chaque salle (en commentaires)
    # Salle1: 120
    # Salle2: 80

    salle_capacite = {"Salle1": 120, "Salle2": 80}

    for film in films:
        if film['score_pred'] is not None:
            film['pred_spect_daily'] = (film['score_pred'] / 2000) / 7
            for salle, capacite in salle_capacite.items():
                # Calcul de pred_rct_daily avec une limite de capacité
                # La limite pour Salle1 est 120, donc si pred_spect_daily * 10 dépasse 120, nous utilisons 120
                # La limite pour Salle2 est 80, donc si pred_spect_daily * 10 dépasse 80, nous utilisons 80
                film['pred_rct_daily_' + salle] = min(film['pred_spect_daily'] * 10, capacite)  
                film['pred_rct_weekly_' + salle] = film['pred_rct_daily_' + salle] * 7
                film['pred_bnf_hebdo_' + salle] = (-4900 + film['pred_rct_weekly_' + salle])
        else:
            film['pred_spect_daily'] = None
            for salle in salle_capacite.keys():
                film['pred_rct_daily_' + salle] = None
                film['pred_rct_weekly_' + salle] = None
                film['pred_bnf_hebdo_' + salle] = None

    context = {
        'films': films,
        'salle_capacite': salle_capacite,
    }

    return render(request, "functionalities/recettes_page.html", context)

def get_data(request):
    # Récupération du titre du film envoyé depuis la requête GET
    film_title = request.GET.get('film')

    # Filtrage des films par titre
    films = FilmScrap.objects.filter(title=film_title)

    # Exemples de limites de capacité pour chaque salle
    salle_capacite = {"Salle1": 120, "Salle2": 80}

    films_data = []

    for film in films:
        film_data = {
            'title': film.title,
            'id': film.id,
            'score_pred': film.score_pred,
            # Calcul de pred_spect_daily avec une limite de capacité
            'pred_spect_daily': min((film.score_pred / 2000) / 7, salle_capacite[salle]) if film.score_pred is not None else None,
        }
        for salle, capacite in salle_capacite.items():
            # Calcul de pred_rct_daily avec une limite de capacité
            # La limite pour Salle1 est 120, donc si pred_spect_daily * 10 dépasse 120, nous utilisons 120
            # La limite pour Salle2 est 80, donc si pred_spect_daily * 10 dépasse 80, nous utilisons 80
            film_data['pred_rct_daily_' + salle] = min(film_data['pred_spect_daily'] * 10, capacite) if film_data['pred_spect_daily'] is not None else None
            film_data['pred_rct_weekly_' + salle] = film_data['pred_rct_daily_' + salle] * 7 if film_data['pred_rct_daily_' + salle] is not None else None
            film_data['pred_bnf_hebdo_' + salle] = (-4900 + film_data['pred_rct_weekly_' + salle]) if film_data['pred_rct_weekly_' + salle] is not None else None

        films_data.append(film_data)

    response_data = {
    "films": films_data
    }
    return JsonResponse(response_data)



@login_required
def predict_page(request):
    today = timezone.now().date()
    one_week_later = today + timedelta(days=7)
    next_day = today + timedelta(days=1)

    films = FilmScrap.objects.filter(date__range=(next_day, one_week_later)).order_by("-score_pred")


    ranking = 1

    for film in films:

        if film.score_pred is not None:
            film.classement = ranking
            ranking += 1
        else:
            film.classement = None

        if film.score_pred is not None:
            film.score_pred_divided = round(film.score_pred / 2000, 2)
        else:
            film.score_pred_divided = None

        if film.score_pred_divided is not None:
            film.score_pred_divided_divided = round(film.score_pred_divided / 7, 2)
        else:
            film.score_pred_divided_divided = None

        if film.score_pred_divided_divided is not None:
            film.recette_journaliere = round(min(film.score_pred_divided_divided * 10, 2000), 2)
        else:
            film.recette_journaliere = None

        if film.recette_journaliere is not None:
            film.recette_hebdomadaire = round(film.recette_journaliere * 7, 2)
        else:
            film.recette_hebdomadaire = None
        
        if film.recette_hebdomadaire is not None:
            film.benefice_hebdomadaire = round(film.recette_hebdomadaire - 4900, 2)
        else:
            film.benefice_hebdomadaire = None
    
    return render(request, "functionalities/prediction_page.html", {"films": films})


@login_required
def historique_page(request):
    return render(request, 'functionalities/historique_page.html')


@login_required
def nouveautes_page(request):
    today = timezone.now().date()
    one_week_later = today + timedelta(days=7)
    next_day = today + timedelta(days=1)

    films = FilmScrap.objects.filter(date__range=(next_day, one_week_later)).order_by("-score_pred")[:10]
    fmt = '{0.hours}h {0.minutes}'

    ranking = 1

    for film in films:
        if film.score_pred is not None:
            film.classement = ranking
            ranking += 1
        else:
            film.classement = None

        if film.duration is not None:
            film.duration = fmt.format(rd(seconds=film.duration))
        if isinstance(film.genre, list):
            film.genre = ', '.join(film.genre)
        if isinstance(film.casting, list):
            film.casting = ', '.join(film.casting)
            film.casting = capitalize_name(film.casting)  
        if isinstance(film.director, list):
            film.director = ', '.join(film.director)
            film.director = capitalize_name(film.director)  
        else:
            film.director = capitalize_name(film.director)  
    
    return render(request, "functionalities/nouveautes_page.html", {"films": films})
