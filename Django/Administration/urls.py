#Administration/urls.py
from django.urls import path
from Administration.views import login, views, signup

app_name = 'Administration'

urlpatterns = [
    path('login/', login.CustomLoginView.as_view(), name='login'),
    path('signup/', signup.create_custom_user, name='signup'),
    path('logout/', views.custom_logout, name='custom_logout'),
]