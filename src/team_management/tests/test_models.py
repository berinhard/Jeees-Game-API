from django.test import TestCase
from django.contrib.auth.models import User

from team_management.models import Team, GameTeam
from game_config.models import Game, Player
from utils.test_helpers import JeeesGameAPITestCase


class TestTeamModel(TestCase):

    def setUp(self):
        self.params = {
            'name':'team_test',
            'description':'team description',
            'development_points':3,
            'testing_points':3,
            'bug_hit':1/3,
            'salary':10,
            'contract_cost':1,
        }

    def test_creates_uuid_on_save(self):
        team = Team(**self.params)
        self.assertFalse(team.uuid)
        team.save()
        self.assertTrue(team.uuid)

    def test_set_team_uuid_on_creation(self):
        team = Team.objects.create(**self.params)
        self.assertTrue(team.uuid)

    def test_doesnt_overrides_team_uuid_after_save(self):
        team = Team.objects.create(**self.params)
        uuid = team.uuid
        team.name = 'new name'
        team.save()
        self.assertEqual(uuid, team.uuid)


class TestGameTeamModel(JeeesGameAPITestCase):

    fixtures = ['teams']

    def setUp(self):
        user, password = self.create_django_user()
        game, player = self.create_game_and_player(user)
        team = Team.objects.all()[0]
        self.game_team = GameTeam.objects.create(team=team, player=player)

    def test_game_salary_return_team_salary_if_was_bought_one_time(self):
        self.game_team.times_bought = 1
        self.game_team.save()
        self.assertEqual(self.game_team.game_salary, self.game_team.team.salary)

    def test_game_salary_return_team_salary_plus_contract_cost_if_was_bought_two_times(self):
        self.game_team.times_bought = 2
        self.game_team.save()
        expected_salary = self.game_team.team.salary + 2 * self.game_team.team.contract_cost
        self.assertEqual(self.game_team.game_salary, expected_salary)
