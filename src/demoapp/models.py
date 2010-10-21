from django.db import models
from django.contrib.auth.models import User

class DemoModel(models.Model):

    name = models.CharField(blank=True, max_length=80)
    email = models.EmailField(blank=True)
    birthday = models.DateField(blank=True, null=True)
