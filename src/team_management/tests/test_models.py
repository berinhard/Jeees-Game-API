from django.test import TestCase

from team_management.models import Team

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
