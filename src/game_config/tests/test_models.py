from django.test import TestCase
from django.contrib.auth.models import User

from game_config.models import Game, Player

__all__ = [
    'GameModelTest',
    'PlayerModelTest',
]

class GameModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()

    def test_creates_uuid_and_admin_token_on_save(self):
        game = Game(name='test', creator=self.user)
        self.assertFalse(game.uuid)
        self.assertFalse(game.admin_token)
        game.save()
        self.assertTrue(game.uuid)
        self.assertTrue(game.admin_token)

    def test_set_creates_uuid_and_admin_token_on_creation(self):
        game = Game.objects.create(name='test', creator=self.user)
        self.assertTrue(game.uuid)
        self.assertTrue(game.admin_token)

    def test_doesnt_overrides_uuid_and_admin_token_after_save(self):
        game = Game.objects.create(name='test', creator=self.user)
        uuid = game.uuid
        admin_token = game.admin_token
        game.name = 'second_name'
        game.save()
        self.assertEqual(uuid, game.uuid)
        self.assertTrue(admin_token, game.admin_token)

class PlayerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
        self.game = Game.objects.create(name='test', creator=self.user)

    def test_creates_uuid_on_save(self):
        player = Player(user=self.user, current_game=self.game)
        self.assertFalse(player.uuid)
        player.save()
        self.assertTrue(player.uuid)

    def test_set_creates_uuid_on_creation(self):
        player = Player.objects.create(user=self.user, current_game=self.game)
        self.assertTrue(player.uuid)

    def test_doesnt_overrides_uuid_after_save(self):
        player = Player.objects.create(user=self.user, current_game=self.game)
        uuid = player.uuid
        player.name = 'second_name'
        player.save()
        self.assertEqual(uuid, player.uuid)
