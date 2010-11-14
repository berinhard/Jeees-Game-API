from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from game_config.models import Game, Player
from project_management.models import Project
from utils.test_helpers import build_http_auth_header


class TestGetNewProject(TestCase):

    fixtures = ['projects']

    def setUp(self):
        password = 'password'
        self.user = User.objects.create_user(
            username='username',
            password=password,
            email='a@a.com'
        )
        self.http_authorization = build_http_auth_header(self.user.username, password)
        self.game = Game.objects.create(name='test', creator=self.user)
        player = Player.objects.create(user=self.user, current_game=self.game)

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
        new_user = User.objects.create_user(
            username='new_username',
            password='password',
            email='new_a@a.com'
        )
        http_authorization = build_http_auth_header('new_username', 'password')

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_doesnt_belong_to_the_game(self):
        new_user = User.objects.create_user(
            username='new_username',
            password='password',
            email='new_a@a.com'
        )
        new_game = Game.objects.create(name='new game', creator=new_user)
        Player.objects.create(user=new_user, current_game=new_game)
        http_authorization = build_http_auth_header('new_username', 'password')

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
        player = Player.objects.get(user=self.user)

        self.assertTrue(player.project)

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
        new_user = User.objects.create_user(
            username='new_username',
            password='password',
            email='new_a@a.com'
        )
        new_player = Player.objects.create(user=new_user, current_game=self.game)
        new_player.project = Project.objects.get(id=1)
        new_player.save()

        response = self.client.get(
            reverse('projects:get_project', kwargs={'game_uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = self.http_authorization
        )
        player_project = Player.objects.get(user=self.user).project

        self.assertNotEqual(player_project, new_player.project)
