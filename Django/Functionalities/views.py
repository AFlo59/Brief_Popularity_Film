from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def estimation_page(request):
    return render(request, "functionalities/estimation_page.html")

@login_required
def predict_page(request):
    return render(request, "functionalities/prediction_page.html")
