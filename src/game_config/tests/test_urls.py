from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game_config.models import Game

__all__ = [
    'GameRootTests',
    'GameInfoURLTests',
]

class GameRootTests(TestCase):

    def test_post_does_not_return_405(self):
        response = self.client.post(reverse('game_config:root'))
        self.assertNotEquals(response.status_code, 405)

    def test_get_does_not_return_405(self):
        response = self.client.get(reverse('game_config:root'))
        self.assertNotEquals(response.status_code, 405)

    def test_delete_return_status_code_405(self):
        response = self.client.delete(reverse('game_config:root'))
        self.assertEquals(response.status_code, 405)

class GameInfoURLTests(TestCase):

    def setUp(self):
        game = Game.objects.create(name='test', creator=User.objects.create())
        self.game_uuid = game.uuid

    def test_post_does_not_return_405(self):
        response = self.client.post(reverse(
            'game_config:game_info',
            kwargs={'uuid':self.game_uuid}
        ))
        self.assertNotEquals(response.status_code, 405)

    def test_get_does_not_return_405(self):
        response = self.client.get(reverse(
            'game_config:game_info',
            kwargs={'uuid':self.game_uuid}
        ))
        self.assertNotEquals(response.status_code, 405)

    def test_delete_does_not_returns_405(self):
        response = self.client.delete(reverse(
            'game_config:game_info',
            kwargs={'uuid':self.game_uuid}
        ))
        self.assertNotEqual(response.status_code, 405)
