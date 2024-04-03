from django.shortcuts import render


def home_page(request):
    return render(request, "main/home_page.html")


# Create your views here.
def history_page(request):
    return render(request, "main/history_page.html")
