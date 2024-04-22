# Administration/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
 