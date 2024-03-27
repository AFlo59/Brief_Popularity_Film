from django.urls import path
from .views import CustomUserCreateView, CustomUserActivationView

urlpatterns = [
    path('signup/', CustomUserCreateView.as_view(), name='signup'),
    path('activate/', CustomUserActivationView.as_view(), name='activate'),
]