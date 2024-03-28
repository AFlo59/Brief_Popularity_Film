# Administration/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=50) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username