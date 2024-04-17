import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FilmScrap
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime, timedelta
from django.utils import timezone



def capitalize_name(name):
    if name:
        return ' '.join([part.capitalize() for part in name.split(' ')])
    return None


def recettes_page(request):
    today = timezone.now().date()
    one_week_later = today + timedelta(days=7)
    next_day = today + timedelta(days=1)

    films = FilmScrap.objects.filter(date__range=(next_day, one_week_later)).order_by("-score_pred")

    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    salle_capacite = {"Salle1": 120, "Salle2": 80}

    for film in films:
        film.pred_spectateur_daily = film.score_pred / 2000 / 7 if film.score_pred is not None else None

    # Organiser les films disponibles par jour et par salle
    films_disponibles = {jour: {'Salle1': [], 'Salle2': []} for jour in jours_semaine}

    for film in films:
        for jour in jours_semaine:
            for salle in salle_capacite:
                capacite = salle_capacite[salle]
                if not films_disponibles[jour][salle] and film.pred_spectateur_daily and film.pred_spectateur_daily >= capacite * 0.5:
                    if any(film in films_disponibles[jour][autre_salle] for autre_salle in salle_capacite if autre_salle != salle):
                        capacite_autre_salle = salle_capacite[[autre_salle for autre_salle in salle_capacite if autre_salle != salle][0]]
                        film.pred_spectateur_daily -= capacite_autre_salle
                    films_disponibles[jour][salle].append(film)

    return render(request, "functionalities/recettes_page.html", {"jours_semaine": jours_semaine, "salle_capacite": salle_capacite, "films_disponibles": films_disponibles})

# def get_film_data(request):
#     if request.method == 'POST' and request.is_ajax():
#         film_id = request.POST.get('film_id')
#         salle = request.POST.get('salle')
#         jour = request.POST.get('jour')
        
#         film = FilmScrap.objects.get(pk=film_id)
#         if film.score_pred is not None:
#             pred_spectateur = film.score_pred / 2000 / 7
#             films_selectionnes = FilmScrap.objects.filter(date=jour, id__in=request.POST.getlist('film_id'), score_pred__isnull=False).count()
#             pred_spectateur = min(pred_spectateur, 200 / films_selectionnes) if films_selectionnes > 0 else 0
#             recettes_daily = pred_spectateur * 10
#             recettes_weekly = min(pred_spectateur * 10 * 7, 120 * 10 + 80 * 10)
#             benefice = recettes_weekly - 4900
#         else:
#             pred_spectateur = None
#             recettes_daily = None
#             recettes_weekly = None
#             benefice = None
        
#         data = {
#             'spectateurs': pred_spectateur,
#             'recettes_daily': recettes_daily,
#             'recettes_weekly': recettes_weekly,
#             'benefice': benefice
#         }
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'error': 'Invalid request'})


from datetime import datetime, timedelta
from django.shortcuts import render
from .models import FilmScrap

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
