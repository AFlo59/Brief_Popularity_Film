from django.urls import path
from Functionalities import views

app_name = "Functionalities"

urlpatterns = [
    path("recettes/", views.recettes_page, name="recettes"),
    path("predict/", views.predict_page, name="predict"),
    path("history/", views.historique_page, name="historique"),
    path("news/", views.nouveautes_page, name="nouveautés"),
    path("get_data/", views.get_data, name="get_data"),
    path("shap_graph/", views.shap_graph, name="shap_graph"),
]
