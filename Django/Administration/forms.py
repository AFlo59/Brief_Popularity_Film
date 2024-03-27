from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

class CustomUserActivationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)