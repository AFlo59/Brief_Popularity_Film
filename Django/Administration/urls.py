#Administration/urls.py
from django.urls import path
from Administration.views import login, views, signup

app_name = 'Administration'

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
]