from django.shortcuts import render

# Create your views here.
def history_page(request):
    return render(request, 'main/history_page.html')