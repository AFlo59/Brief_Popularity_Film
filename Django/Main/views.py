from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_page(request):
    return render(request, "main/home_page.html")


# Create your views here.
def history_page(request):
    return render(request, "main/history_page.html")
