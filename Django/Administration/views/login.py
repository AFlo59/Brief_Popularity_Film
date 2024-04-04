#Administration/views/login.py
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect

class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "Vous êtes déjà connecté.")
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Vous vous êtes connecté avec succès.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Vos informations de connexion sont incorrectes. Veuillez réessayer.")
        return super().form_invalid(form)