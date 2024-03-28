# Administration/views/signup.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from Administration.forms import CustomUserCreationForm

@login_required
def create_custom_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Le compte est inactif jusqu'à ce qu'il soit validé
            user.save()

            # Envoyer un email au nouvel utilisateur avec un lien pour finaliser son compte
            send_activation_email(user)

            return redirect('home')  # Redirection vers la page d'accueil ou une autre vue
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_custom_user.html', {'form': form})

def send_activation_email(user):
    # Générer le lien d'activation
    activation_link = f"http://votre_site.com/activate/{user.id}/"

    # Envoyer l'email
    subject = 'Activation de votre compte'
    message = f'Bienvenue sur notre site. Veuillez finaliser votre compte en cliquant sur le lien suivant : {activation_link}'
    sender = 'votre_email@example.com'
    recipient = user.email
    send_mail(subject, message, sender, [recipient])