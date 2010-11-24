import unittest2

from django.test import TestCase
from django.contrib.auth.models import User

from game_config.models import Game, Player


def build_http_auth_header(username, password):
    base_64_string = '%s:%s' % (username, password)
    auth_header = 'Basic ' + base_64_string.encode('base64')
    return auth_header


class JeeesGameAPITestCase(TestCase, unittest2.TestCase):

    def create_django_user(self, username='username', password='password', email='a@a.com'):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user, password

    def create_game_and_player(self, user, game_name='test'):
        game = Game.objects.create(name=game_name, creator=user)
        player = Player.objects.create(user=user, current_game=game)
        return game, player
