from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game_config.models import Game, Player

__all__ = [
    'GameCreationTests',
    'GameDeletionTests',
]

class GameCreationTests(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User(username = self.username)
        self.user.set_password(self.password)
        self.user.save()

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
            {"username":self.username, "password":self.password, "game_name":"name"},
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
            {"username":self.username, "password":self.password},
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
            {"username":self.username, "password":self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)


class GameDeletionTests(TestCase):

    def setUp(self):
        game = Game.objects.create(name='test')
        self.game_uuid = game.uuid

    def test_return_404_if_game_doesnt_exist(self):
        response = self.client.delete(
            reverse('game_config:delete_game', kwargs={'uuid':'1234'})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_game_if_it_exist(self):
        self.assertTrue(Game.objects.all())
        response = self.client.delete(
            reverse('game_config:delete_game', kwargs={'uuid':self.game_uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Game.objects.all())
