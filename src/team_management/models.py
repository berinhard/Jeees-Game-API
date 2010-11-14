import uuid

from django.db import models
from django.db.models.signals import pre_save


class Team(models.Model):

    name = models.CharField(max_length=50)
    development_points = models.IntegerField()
    testing_points = models.IntegerField()
    salary = models.IntegerField()
    cost = models.IntegerField()
    uuid = models.CharField(max_length=36)

def __set_team_uuid_on_creation(sender, **kwargs):
    team = kwargs['instance']
    if not team.pk:
        team.uuid = str(uuid.uuid4())
pre_save.connect(__set_team_uuid_on_creation, sender=Team)
