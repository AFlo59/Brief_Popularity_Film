#urls.py
from django.urls import path
from Functionalities.views import *


app_name = 'Functionalities'

urlpatterns = [
    path('test/', test_view, name='test'),
]