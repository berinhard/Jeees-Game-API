import uuid

from django.db import models
from django.db.models.signals import pre_save

from game_config.models import Player


class Team(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    development_points = models.IntegerField()
    testing_points = models.IntegerField()
    bug_hit = models.DecimalField(max_digits=5, decimal_places=4)
    salary = models.IntegerField()
    contract_cost = models.IntegerField()
    uuid = models.CharField(max_length=36, blank=True)

    def to_dict(self):
        team = {
            'name':self.name,
            'description':self.description,
            'development_points':self.development_points,
            'testing_points':self.testing_points,
            'bug_hit':str(self.bug_hit),
            'salary':self.salary,
            'contract_cost':self.contract_cost,
        }
        return team

def __set_team_uuid_on_creation(sender, **kwargs):
    team = kwargs['instance']
    if not team.pk:
        team.uuid = str(uuid.uuid4())
pre_save.connect(__set_team_uuid_on_creation, sender=Team)


class GameTeam(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    times_bought = models.IntegerField(default=1)
    development = models.BooleanField(default=True)

    @property
    def purchase_price(self):
        return self.team.salary + self.team.contract_cost * self.times_bought

    @property
    def game_salary(self):
        if self.times_bought > 1:
            return self.purchase_price
        else:
            return self.team.salary

    def to_dict(self):
        player_game_dict = self.team.to_dict()
        player_game_dict.update({
            'salary':self.game_salary,
            'owner':self.player.user.username,
        })
        return player_game_dict
