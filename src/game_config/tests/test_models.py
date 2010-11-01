from django.test import TestCase
from django.contrib.auth.models import User

from game_config.models import Game, Player

__all__ = [
    'GameModelTest',
    'PlayerModelTest',
]

class GameModelTest(TestCase):

    def test_creates_uuid_on_save(self):
        game = Game(name='test')
        self.assertFalse(game.uuid)
        game.save()
        self.assertTrue(game.uuid)

    def test_set_creates_uuid_on_creation(self):
        game = Game.objects.create(name='test')
        self.assertTrue(game.uuid)

    def test_doesnt_overrides_uuid_after_save(self):
        game = Game.objects.create(name='test')
        uuid = game.uuid
        game.name = 'second_name'
        game.save()
        self.assertEqual(uuid, game.uuid)

class PlayerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
        self.game = Game.objects.create(name='test')

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
