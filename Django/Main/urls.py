from django.urls import path
from main import views


urlpatterns = [
    path('history/', views.history_page, name='history'),
]