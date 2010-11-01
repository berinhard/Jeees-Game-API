import uuid

from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):

    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super(Game, self).save(*args, **kwargs)


class Player(models.Model):

    user = models.OneToOneField(User)
    current_game = models.ForeignKey(Game)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super(Player, self).save(*args, **kwargs)
