from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from utils.test_helpers import build_http_auth_header
from game_config.models import Game, Player
from team_management.models import Team

__all__ = [
    'BuyTeamTests',
]


class BuyTeamTests(TestCase):

    fixtures = ['teams']

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
        self.team = Team.objects.all()[0]

    def test_return_unauthorized_with_wrong_credentials(self):
        http_authorization = build_http_auth_header(self.user.username, 'wrong')

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization,
        )

        self.assertEqual(response.status_code, 401)

    def test_return_404_if_team_does_not_exist(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 404)

    def test_return_bad_request_if_no_json_or_corrupted_json_object(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'}),
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 400)

    def test_return_bad_request_with_missing_json_parameters(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 400)

    def test_return_404_if_game_does_not_exist(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':'1234'},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_has_no_player(self):
        new_user = User.objects.create_user(
            username='new_username',
            password='password',
            email='new_a@a.com'
        )
        http_authorization = build_http_auth_header('new_username', 'password')

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization,
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

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization,
        )

        self.assertEqual(response.status_code, 404)

