from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game_config.models import Game

__all__ = [
    'GameCreationTests'
]

class GameCreationTests(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        user = User(username = self.username)
        user.set_password(self.password)
        user.save()

    def test_return_bad_request_if_missing_login_or_password_on_post(self):
        response = self.client.post(reverse('game_config:create_game'), {"username":"user"}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_return_unauthorized_with_wrong_credentials(self):
        response = self.client.post(reverse('game_config:create_game'), {"username":"wrong", "password":'wrong'}, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_creates_new_game_with_corret_credentials(self):
        self.assertFalse(Game.objects.all())

        response = self.client.post(reverse('game_config:create_game'), {"username":self.username, "password":self.password}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all())
