# -*- encoding:utf-8 -*-
import json
from mock import patch, Mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from game_config.models import Game, Player
from team_management.models import GameTeam, Team
from project_management.models import Project
from utils.test_helpers import build_http_auth_header, JeeesGameAPITestCase

__all__ = [
    'TestGetNewProject',
    'TestGetProjectInfo',
    'TestWorkOnRelease',
]

class TestGetNewProject(JeeesGameAPITestCase):

    fixtures = ['projects']

    def setUp(self):
        self.user, password = self.create_django_user()
        self.http_authorization = build_http_auth_header(self.user.username, password)
        self.game, player = self.create_game_and_player(self.user)

    def test_return_unauthorized_with_wrong_credentials(self):
        http_authorization = build_http_auth_header(self.user.username, 'wrong')

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 401)

    def test_return_404_if_game_doesnt_exist(self):
        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':'1234'}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_has_no_player(self):
        new_user, password = self.create_django_user(username='new')
        http_authorization = build_http_auth_header(new_user.username, password)

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_doesnt_belong_to_the_game(self):
        new_user, password = self.create_django_user(username='new')
        game, player = self.create_game_and_player(new_user, game_name='new_game')
        http_authorization = build_http_auth_header(new_user.username, password)

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_player_gets_a_new_project(self):
        player = Player.objects.get(user=self.user)
        self.assertFalse(player.project)

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        content = json.loads(response.content)

        player = Player.objects.get(user=self.user)
        self.assertTrue(player.project)
        self.assertTrue(content['project_info_uri'])

    def test_return_403_player_already_have_a_project(self):
        player = Player.objects.get(user=self.user)
        player.project = Project.objects.get(id=1)
        player.save()

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )

        self.assertEqual(response.status_code, 403)

    def test_cant_repeat_same_project_for_more_than_one_player(self):
        new_user, password = self.create_django_user(username='new')
        new_player = Player.objects.create(user=new_user, current_game=self.game)
        new_player.project = Project.objects.get(id=1)
        new_player.save()

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        player_project = Player.objects.get(user=self.user).project

        self.assertNotEqual(player_project, new_player.project)

    #teste de regressão
    def test_player_cash_gets_updated(self):
        player = Player.objects.get(user=self.user)
        self.assertEqual(player.cash, 0)

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )

        player = Player.objects.get(user=self.user)
        self.assertEqual(player.cash, player.project.initial_cash)


class TestGetProjectInfo(TestCase):

    fixtures = ['projects', 'releases']

    def test_returns_404_if_project_does_not_exist(self):
        response = self.client.get(reverse(
            'projects:project_info', kwargs={'proj_uuid':'1234'}
        ))

        self.assertEqual(response.status_code, 404)

    def test_return_project_info_if_it_exists(self):
        uuid = Project.objects.all()[0].uuid
        response = self.client.get(reverse(
            'projects:project_info', kwargs={'proj_uuid':uuid}
        ))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['name'])
        self.assertTrue(content['description'])
        self.assertTrue(content['quality'])
        self.assertTrue(content['initial_cash'])
        self.assertTrue(content['uuid'])
        self.assertTrue(content['releases'])
        self.assertTrue(content['releases'][0]['position'])
        self.assertTrue(content['releases'][0]['payment'])
        self.assertTrue(content['releases'][0]['component_1'])
        self.assertTrue(content['releases'][0]['component_2'])
        self.assertTrue(content['releases'][0]['component_3'])
        self.assertTrue(content['releases'][0]['component_4'])


class TestWorkOnRelease(JeeesGameAPITestCase):

    fixtures = ['projects', 'releases', 'teams']

    def setUp(self):
        self.user, password = self.create_django_user()
        self.http_authorization = build_http_auth_header(self.user.username, password)
        self.game, self.player = self.create_game_and_player(self.user)
        self.game_team = GameTeam.objects.create(team=Team.objects.all()[0], player=self.player)

    def test_return_unauthorized_with_wrong_credentials(self):
        http_authorization = build_http_auth_header(self.user.username, 'wrong')

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 401)

    def test_return_404_if_game_doesnt_exist(self):
        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':'1234'}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_has_no_player(self):
        new_user, password = self.create_django_user(username='new')
        http_authorization = build_http_auth_header(new_user.username, password)

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_doesnt_belong_to_the_game(self):
        new_user, password = self.create_django_user(username='new')
        game, player = self.create_game_and_player(new_user, game_name='new_game')
        http_authorization = build_http_auth_header(new_user.username, password)

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_400_if_user_doesnt_have_any_team(self):
        GameTeam.objects.all().delete()

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )

        self.assertEqual(response.status_code, 400)

    def test_return_400_if_user_doesnt_have_any_team(self):
        GameTeam.objects.all().delete()

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )

        self.assertEqual(response.status_code, 400)

    @patch('random.randint', Mock(return_value=3))
    def test_return_development_points_if_team_is_developing(self):
        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        content = json.loads(response.content)
        development_points = Team.objects.all()[0].development_points * 3

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['development_points'], development_points)
        self.assertEqual(content['testing_points'], 0)

    @patch('random.randint', Mock(return_value=3))
    def test_return_development_points_if_more_than_one_team_is_developing(self):
        new_team = GameTeam.objects.create(team=Team.objects.all()[1], player=self.player)

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        content = json.loads(response.content)
        development_points = Team.objects.all()[0].development_points * 3
        development_points += Team.objects.all()[1].development_points * 3

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['development_points'], development_points)
        self.assertEqual(content['testing_points'], 0)

    @patch('random.randint', Mock(return_value=3))
    def test_return_testing_points_if_has_only_testing_teams(self):
        new_team = GameTeam.objects.create(team=Team.objects.all()[1], player=self.player, development=False)
        self.game_team.development=False
        self.game_team.save()

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        content = json.loads(response.content)
        testing_points = Team.objects.all()[0].testing_points * 3
        testing_points += Team.objects.all()[1].testing_points * 3

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['development_points'], 0)
        self.assertEqual(content['testing_points'], testing_points)

    @patch('random.randint', Mock(return_value=3))
    def test_return_testing_and_development_points_if_has_both_teams(self):
        new_team = GameTeam.objects.create(team=Team.objects.all()[1], player=self.player, development=False)

        response = self.client.get(
            reverse('projects:calc_pontuation', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        content = json.loads(response.content)
        development_points = Team.objects.all()[1].testing_points * 3
        testing_points = Team.objects.all()[1].testing_points * 3

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['development_points'], development_points)
        self.assertEqual(content['testing_points'], testing_points)
