import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FilmScrap
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse

# Exemples de limites de capacité pour chaque salle (en commentaires)
# Salle1: 120
# Salle2: 80
SALLE_CAPACITE = {"Salle1": 120, "Salle2": 80}
def calculate_charge_value(salle):
    return 4900 * 0.6 if salle == "Salle1" else 4900 * 0.4


def capitalize_name(name):
    if name:
        return " ".join([part.capitalize() for part in name.split(" ")])
    return None


def recettes_page(request):
    today = datetime.now().date()
    current_weekday = today.weekday()

    days_until_wednesday = (2 - current_weekday) % 7
    wednesday_this_week = today + timedelta(days=days_until_wednesday)
    next_tuesday = wednesday_this_week + timedelta(days=6)

    films = (
        FilmScrap.objects.filter(date__gte=wednesday_this_week, date__lte=next_tuesday)
        .order_by("-score_pred")
        .values("title", "id", "score_pred")
    )

    for film in films:
        if film["score_pred"] is not None:
            film["pred_spect_daily"] = (film["score_pred"] / 2000) / 7
            for salle, capacite in SALLE_CAPACITE.items():
                charge_value_temp = calculate_charge_value(salle)
            
                film["pred_rct_daily_" + salle] = round(min(
                    film["pred_spect_daily"] * 10, capacite * 10
                ), 2)
                film["pred_rct_weekly_" + salle] = round(film["pred_rct_daily_" + salle] * 7, 2)

                film["pred_bnf_hebdo_" + salle] = (
                    round(film["pred_rct_weekly_" + salle] - charge_value_temp ),2
                )
    else:
        film["pred_spect_daily"] = None
        for salle in SALLE_CAPACITE.keys():
            film["pred_rct_daily_" + salle] = None
            film["pred_rct_weekly_" + salle] = None
            film["pred_bnf_hebdo_" + salle] = None

    context = {
        "films": films,
        "salle_capacite": SALLE_CAPACITE,
    }

    return render(request, "functionalities/recettes_page.html", context)


def get_data(request):
    film_id = request.GET.get("film")
    salle = request.GET.get("salle")
    
    charge_value_temp = calculate_charge_value(f"Salle{salle}")

 
    film = FilmScrap.objects.filter(id=film_id).first()

    film_data = {
        "title": film.title,
        "id": film.id,
        "score_pred": film.score_pred,
        "pred_spect_daily": None,
        "pred_rct_daily": None,
        "pred_bnf_hebdo": None,
        "salle" : salle,
        "charge_value_temp": charge_value_temp,
    }

    if film.score_pred is not None:
        pred_spect_daily = film.score_pred / 2000 / 7
        film_data["pred_spect_daily"] = round(min(pred_spect_daily, SALLE_CAPACITE["Salle1"]), 2)

    capacite = SALLE_CAPACITE[f"Salle{salle}"]
    
    film_data["pred_rct_daily"] = (
        int(min(film_data["pred_spect_daily"] * 10, capacite * 10))
        if film_data["pred_spect_daily"] is not None
        else None
    )

    film_data["pred_rct_weekly"] = (
        int(film_data["pred_rct_daily"] * 7)
        if film_data["pred_rct_daily"] is not None
        else None
    )
    
    film_data["pred_bnf_hebdo"] = (
        int(film_data["pred_rct_weekly"] - charge_value_temp)
            if film_data["pred_rct_weekly"] is not None
        else None
    )

    return JsonResponse({"film": film_data})


@login_required
def predict_page(request):
    today = datetime.now().date()
    current_weekday = today.weekday()

    days_until_wednesday = (2 - current_weekday) % 7
    wednesday_this_week = today + timedelta(days=days_until_wednesday)
    next_tuesday = wednesday_this_week + timedelta(days=6)

    films = (
        FilmScrap.objects.filter(date__gte=wednesday_this_week, date__lte=next_tuesday)
        .order_by("-score_pred")
    )

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
            film.recette_journaliere = round(
                min(film.score_pred_divided_divided * 10, 2000), 2
            )
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
    today = datetime.now().date()
    current_weekday = today.weekday()

    days_until_wednesday = (2 - current_weekday) % 7
    wednesday_this_week = today + timedelta(days=days_until_wednesday)
    next_tuesday = wednesday_this_week + timedelta(days=6)

    # Calculate the range of dates from last Tuesday to 6 days before last Tuesday
    start_date = wednesday_this_week - timedelta(days=14)
    end_date = next_tuesday - timedelta(days=7)

    films = (
        FilmScrap.objects.filter(date__gte=start_date, date__lte=end_date)
        .order_by("-score_pred")
    )
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
    return render(request, "functionalities/historique_page.html", {"films": films})


@login_required
def nouveautes_page(request):
    today = datetime.now().date()
    current_weekday = today.weekday()

    days_until_wednesday = (2 - current_weekday) % 7
    wednesday_this_week = today + timedelta(days=days_until_wednesday)
    next_tuesday = wednesday_this_week + timedelta(days=6)

    films = (
        FilmScrap.objects.filter(date__gte=wednesday_this_week, date__lte=next_tuesday)
        .order_by("-score_pred")
    )[:10]
    fmt = "{0.hours}h {0.minutes}"

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
            film.genre = ", ".join(film.genre)
        if isinstance(film.casting, list):
            film.casting = ", ".join(film.casting)
            film.casting = capitalize_name(film.casting)
        if isinstance(film.director, list):
            film.director = ", ".join(film.director)
            film.director = capitalize_name(film.director)
        else:
            film.director = capitalize_name(film.director)

    return render(request, "functionalities/nouveautes_page.html", {"films": films})
