from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FilmScrap

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
    films = FilmScrap.objects.order_by("id")[:10]
    print(films)
    return render(request, "functionalities/nouveautes_page.html", {"films": films})
