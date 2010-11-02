import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game_config.models import Game, Player

__all__ = [
    'GameCreationTests',
    'GameDeletionTests',
    'JoinGameTests',
    'GetGameInfoTests',
]

class GameCreationTests(TestCase):

    def setUp(self):
        self.password = 'password'
        self.user = User.objects.create_user(
            username='username', email='a@a.com', password=self.password
        )

    def test_return_bad_request_if_missing_login_or_password_on_post(self):
        response = self.client.post(
            reverse('game_config:create_game'),
            {"username":"user"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_return_unauthorized_with_wrong_credentials(self):
        response = self.client.post(
            reverse('game_config:create_game'),
            {"username":"wrong", "password":'wrong'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_creates_new_game_with_corret_credentials_and_game_info(self):
        self.assertFalse(Game.objects.all())
        self.assertFalse(Player.objects.all())

        response = self.client.post(
            reverse('game_config:create_game'),
            {"username":self.user.username, "password":self.password, "game_name":"name"},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all())
        self.assertTrue(Player.objects.all())

    def test_creates_new_game_with_corret_credentials_and_without_game_info(self):
        self.assertFalse(Game.objects.all())
        self.assertFalse(Player.objects.all())

        response = self.client.post(
            reverse('game_config:create_game'),
            {"username":self.user.username, "password":self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all())
        self.assertTrue(Player.objects.all())

    def test_return_forbiden_in_case_user_is_already_in_a_game(self):
        game = Game.objects.create(name='test')
        player = Player.objects.create(user=self.user, current_game=game)

        response = self.client.post(
            reverse('game_config:create_game'),
            {"username":self.user.username, "password":self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)

    def test_succefull_response_returns_correct_content(self):
        response = self.client.post(
            reverse('game_config:create_game'),
            {"username":self.user.username, "password":self.password, "game_name":"name"},
            content_type='application/json'
        )
        content = json.loads(response.content)

        self.assertTrue('game' in content)
        self.assertTrue(content['game'])
        self.assertTrue('delete_uri' in content)


class GameDeletionTests(TestCase):

    def setUp(self):
        game = Game.objects.create(name='test')
        self.game_uuid = game.uuid
        self.game_admin_token = game.admin_token

    def test_return_404_if_game_doesnt_exist(self):
        response = self.client.delete(reverse(
            'game_config:delete_game',
            kwargs={'uuid':'1234', 'admin_token':self.game_admin_token}
        ))
        self.assertEqual(response.status_code, 404)

    def test_return_404_with_incorrect_admin_token(self):
        response = self.client.delete(reverse(
            'game_config:delete_game',
            kwargs={'uuid':self.game_uuid, 'admin_token':'12345'}
        ))
        self.assertEqual(response.status_code, 404)

    def test_delete_game_if_it_exist_and_correct_admin_token_is_given(self):
        self.assertTrue(Game.objects.all())
        response = self.client.delete(reverse(
            'game_config:delete_game',
            kwargs={'uuid':self.game_uuid, 'admin_token':self.game_admin_token})
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Game.objects.all())


class JoinGameTests(TestCase):

    def setUp(self):
        self.password = '123456'
        self.user = User.objects.create_user(
            username='name', email='a@a.com', password=self.password
        )

        self.game = Game.objects.create(name='teste')

    def test_return_bad_request_if_missing_login_or_password_on_post(self):
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {"username":"user"},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_return_unauthorized_with_wrong_credentials(self):
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {"username":"wrong", "password":'wrong'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_returns_404_if_game_doesnt_exist(self):
        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':'not_exists'}),
            {"username":self.user.username, "password":self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)

    def test_returns_forbidden_in_case_user_is_already_in_a_game(self):
        player = Player.objects.create(user=self.user, current_game=self.game)

        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {"username":self.user.username, "password":self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)

    def test_join_game_with_correct_credentials(self):
        self.assertFalse(Player.objects.all())

        response = self.client.post(
            reverse('game_config:game_info', kwargs={'uuid':self.game.uuid}),
            {"username":self.user.username, "password":self.password},
            content_type='application/json'
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
        self.game = Game.objects.create(name='teste')
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
