from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):

    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=32)

class Player(models.Model):

    user = models.OneToOneField(User)
    current_game = models.ForeignKey(Game)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_lengh=32)
