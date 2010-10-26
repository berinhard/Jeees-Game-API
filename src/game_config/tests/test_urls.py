from django.test import TestCase
from django.core.urlresolvers import reverse

__all__ = [
    'GameCreationURLTests',
]

class GameCreationURLTests(TestCase):

    def test_post_does_not_return_405(self):
        response = self.client.post(reverse('game_config:create_game'))
        self.assertNotEquals(response.status_code, 405)

    def test_get_return_status_code_405(self):
        response = self.client.get(reverse('game_config:create_game'))
        self.assertEquals(response.status_code, 405)
