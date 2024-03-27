from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomUserActivationForm

User = get_user_model()

class CustomUserCreateView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(User.objects.make_random_password()) # Generate random password
        user.save()
        self.send_activation_email(user)
        return super().form_valid(form)

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = _('Activate Your Account')
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject, message, None, [user.email])

class CustomUserActivationView(FormView):
    template_name = 'registration/activation.html'
    form_class = CustomUserActivationForm

    def form_valid(self, form):
        # Activation logic here
        return super().form_valid(form)