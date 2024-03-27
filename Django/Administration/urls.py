from django.urls import path
from Administration.views import login, views

app_name = 'Administration'

urlpatterns = [
    path('signup/', views.CustomUserCreateView.as_view(), name='signup'),
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    # path('activate/', CustomUserActivationView.as_view(), name='activate'),
]