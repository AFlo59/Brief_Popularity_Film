from django.conf import settings
from django.db import models

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
