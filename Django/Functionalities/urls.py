from django.urls import path
from Functionalities import views

urlpatterns = [
    path('predict/', views.predict_page, name='predict'),
]