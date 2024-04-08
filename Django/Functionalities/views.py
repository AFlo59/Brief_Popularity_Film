from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Film
from .models import Historique

@login_required
def recettes_page(request):
    return render(request, "functionalities/recettes_page.html")

@login_required
def predict_page(request):
    return render(request, "functionalities/prediction_page.html")

@login_required
def historique_page(request):

    historiques = Historique.objects.all()
    return render(request, 'functionalities/historique_page.html', {'historiques': historiques})

@login_required
def nouveautes_page(request):
    films = Film.objects.order_by('classement')[:10]
    return render(request, 'functionalities/nouveautes_page.html', {'films': films})
