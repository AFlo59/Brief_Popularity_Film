from django.urls import path
from Functionalities import views

urlpatterns = [
    path('estimation/', views.estimation_page, name='estimation'),
    
]