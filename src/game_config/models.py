import uuid
from hashlib import md5

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from project_management.models import Project

class Game(models.Model):

    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=36)
    creator = models.OneToOneField(User)

    def to_dict(self):
        return {'name':self.name, 'uuid':self.uuid}

def __set_game_uuid_on_creation(sender, **kwargs):
    game = kwargs['instance']
    if not game.pk:
        game.uuid = str(uuid.uuid4())
pre_save.connect(__set_game_uuid_on_creation, sender=Game)


class Player(models.Model):

    user = models.OneToOneField(User)
    current_game = models.ForeignKey(Game)
    timestamp = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    cash = models.IntegerField(default=0)
    uuid = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super(Player, self).save(*args, **kwargs)
