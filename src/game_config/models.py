import uuid
from hashlib import md5

from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):

    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=36)
    admin_token = models.CharField(max_length=32)
    creator = models.OneToOneField(User)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        if not self.admin_token:
            hashable_string = self.uuid + str(self.timestamp)
            self.admin_token = md5(hashable_string).hexdigest()
        super(Game, self).save(*args, **kwargs)

    def to_dict(self):
        return {'name':self.name, 'uuid':self.uuid}


class Player(models.Model):

    user = models.OneToOneField(User)
    current_game = models.ForeignKey(Game)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super(Player, self).save(*args, **kwargs)
