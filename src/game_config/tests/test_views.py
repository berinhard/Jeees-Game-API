import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game_config.models import Game, Player
from utils.test_helpers import build_http_auth_header

__all__ = [
    'GameCreationTests',
    'GameDeletionOrLeaveTests',
    'JoinGameTests',
    'GetGameInfoTests',
]

class GameCreationTests(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username, email='a@a.com', password=self.password
        )

    def test_return_unauthorized_with_wrong_credentials(self):
        http_authorization = build_http_auth_header(self.username, 'wrong')
        response = self.client.post(
            reverse('game_config:create_game'),
            {'game_name':'name'},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 401)

    def test_creates_new_game_with_corret_credentials_and_game_info(self):
        self.assertFalse(Game.objects.all())
        self.assertFalse(Player.objects.all())

        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:create_game'),
            {"game_name":"name"},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all())
        self.assertTrue(Player.objects.all())
        game = Game.objects.all()[0]
        self.assertTrue(game.creator, self.user)

    def test_bad_request_with_corret_credentials_and_without_game_info(self):
        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:create_game'),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 400)

    def test_return_forbiden_in_case_user_is_already_in_a_game(self):
        game = Game.objects.create(name='test', creator=User.objects.create())
        player = Player.objects.create(user=self.user, current_game=game)

        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:create_game'),
            {"game_name":"name"},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)

    def test_succefull_response_returns_correct_content(self):
        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:create_game'),
            {"game_name":"name"},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )
        content = json.loads(response.content)

        self.assertTrue(content['game'])
        self.assertTrue('delete_uri' in content)


class GameDeletionOrLeaveTests(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        user = User.objects.create_user(
            username=self.username, email='a@a.com', password=self.password
        )
        self.game = Game.objects.create(name='test', creator=user)

    def test_return_404_if_game_doesnt_exist(self):
        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.delete(
            reverse('game_config:game_info', kwargs={'uuid':'1234'}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 404)

    def test_return_401_with_incorrect_login(self):
        http_authorization = build_http_auth_header(self.username, 'wrong')
        response = self.client.delete(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_game_if_it_exist_and_is_creator_login(self):
        self.assertTrue(Game.objects.all())

        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.delete(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Game.objects.all())

    def test_leave_game_if_it_exist_and_player_login(self):
        user = User.objects.create_user(
            username='user', email='a@a.com', password='password'
        )
        player = Player.objects.create(user=user, current_game=self.game)

        self.assertTrue(Game.objects.all())
        self.assertTrue(Player.objects.all())

        http_authorization = build_http_auth_header('user', 'password')
        response = self.client.delete(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all())
        self.assertFalse(Player.objects.all())

    def test_404_player_does_not_belong_to_the_game(self):
        user = User.objects.create_user(
            username='user2', email='a@a.com', password='password2'
        )
        game = Game.objects.create(name='game_2', creator=user)
        player = Player.objects.create(user=user, current_game=game)

        self.assertTrue(Game.objects.all())
        self.assertTrue(Player.objects.all())

        http_authorization = build_http_auth_header('user2', 'password2')
        response = self.client.delete(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Game.objects.all())
        self.assertTrue(Player.objects.all())


class JoinGameTests(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username, email='a@a.com', password=self.password
        )

        self.game = Game.objects.create(name='teste', creator=self.user)

    def test_return_unauthorized_with_wrong_credentials(self):
        http_authorization = build_http_auth_header(self.username, 'wrong')
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 401)

    def test_returns_404_if_game_doesnt_exist(self):
        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':'not_exists'}),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 404)

    def test_returns_forbidden_in_case_user_is_already_in_a_game(self):
        player = Player.objects.create(user=self.user, current_game=self.game)

        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )

        self.assertEqual(response.status_code, 403)

    def test_join_game_with_correct_credentials(self):
        self.assertFalse(Player.objects.all())

        http_authorization = build_http_auth_header(self.username, self.password)
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Player.objects.all())
        self.assertTrue('game' in content)
        self.assertTrue(content['game'])


class GetGameInfoTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='name',
            email='a@a.com',
            password='123456',
        )
        self.game = Game.objects.create(name='teste', creator=user)
        Player.objects.create(user=user, current_game=self.game)

    def test_returns_404_if_game_doesnt_exist(self):
        response = self.client.get(
            reverse('game_config:game_info', kwargs={'uuid':'wrong'})
        )

        self.assertEqual(response.status_code, 404)

    def test_return_game_info_for_existent_game(self):
        response = self.client.get(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid})
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['game'])
        self.assertTrue(isinstance(content['players'], list))
        self.assertTrue(content['players'])
        self.assertTrue(content['players'][0]['uuid'])
        self.assertTrue(content['players'][0]['username'])
