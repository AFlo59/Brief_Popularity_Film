#Administration/views/login.py
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Main:home')


        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Votre logique de traitement après une connexion réussie
        # Par exemple, rediriger l'utilisateur vers une page spécifique
        messages.success(self.request, 'You have been successfully logged in.')
        return redirect('Main:home')
    
    def form_invalid(self, form):
        # Votre logique de traitement en cas d'échec de connexion
        # Par exemple, afficher un message d'erreur
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    