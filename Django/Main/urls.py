# urls.py
from django.urls import path
from Main.views import *

app_name = "Main"

urlpatterns = [
    path("", home_page, name="home"),
    path("history/", history_page, name="history"),
]
