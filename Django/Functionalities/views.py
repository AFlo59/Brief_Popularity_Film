from django.shortcuts import render


def estimation_page(request):
    return render(request, "functionalities/estimation_page.html")


def predict_page(request):
    return render(request, "functionalities/prediction_page.html")
