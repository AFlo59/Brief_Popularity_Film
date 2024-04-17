from django.urls import path
from Functionalities import views

app_name = 'Functionalities'

urlpatterns = [
    path("recettes/", views.recettes_page, name="recettes"),
    path("predict/", views.predict_page, name="predict"),
    path("history/", views.historique_page, name="historique"),
    path("news/", views.nouveautes_page, name="nouveautés"),
    # path('get_film_data/', views.get_film_data, name='get_film_data'), 
]