# Administration/views/views.py
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def custom_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'home'))