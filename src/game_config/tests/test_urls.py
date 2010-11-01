from django.test import TestCase
from django.core.urlresolvers import reverse

from game_config.models import Game

__all__ = [
    'GameCreationURLTests',
    'GameDeletionURLTests',
]

class GameCreationURLTests(TestCase):

    def test_post_does_not_return_405(self):
        response = self.client.post(reverse('game_config:create_game'))
        self.assertNotEquals(response.status_code, 405)

    def test_get_return_status_code_405(self):
        response = self.client.get(reverse('game_config:create_game'))
        self.assertEquals(response.status_code, 405)

    def test_delete_return_status_code_405(self):
        response = self.client.delete(reverse('game_config:create_game'))
        self.assertEquals(response.status_code, 405)

class GameDeletionURLTests(TestCase):

    def setUp(self):
        game = Game.objects.create(name='test')
        self.game_uuid = game.uuid

    def test_delete_does_not_return_405(self):
        response = self.client.delete(
            reverse('game_config:delete_game', kwargs={'uuid':self.game_uuid})
        )
        self.assertNotEquals(response.status_code, 405)

    def test_get_returns_405(self):
        response = self.client.get(
            reverse('game_config:delete_game', kwargs={'uuid':self.game_uuid})
        )
        self.assertEqual(response.status_code, 405)

    def test_post_returns_405(self):
        response = self.client.post(
            reverse('game_config:delete_game', kwargs={'uuid':self.game_uuid})
        )
        self.assertEqual(response.status_code, 405)
