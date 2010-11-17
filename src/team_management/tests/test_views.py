from mock import Mock, patch

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from utils.test_helpers import build_http_auth_header
from game_config.models import Game, Player
from team_management.models import Team, GameTeam

__all__ = [
    'BuyTeamTests',
]


class BuyTeamTests(TestCase):

    fixtures = ['teams']

    def setUp(self):
        password = 'password'
        self.user = User.objects.create_user(
            username='username',
            password=password,
            email='a@a.com'
        )
        self.http_authorization = build_http_auth_header(self.user.username, password)
        self.game = Game.objects.create(name='test', creator=self.user)
        self.player = Player.objects.create(user=self.user, current_game=self.game)
        self.team = Team.objects.all()[0]

    def test_return_unauthorized_with_wrong_credentials(self):
        http_authorization = build_http_auth_header(self.user.username, 'wrong')

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization,
        )

        self.assertEqual(response.status_code, 401)

    def test_return_404_if_team_does_not_exist(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 404)

    def test_return_bad_request_if_no_json_or_corrupted_json_object(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'}),
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 400)

    def test_return_bad_request_with_missing_json_parameters(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 400)

    def test_return_404_if_game_does_not_exist(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':'1234'},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_has_no_player(self):
        new_user = User.objects.create_user(
            username='new_username',
            password='password',
            email='new_a@a.com'
        )
        http_authorization = build_http_auth_header('new_username', 'password')

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization,
        )

        self.assertEqual(response.status_code, 404)

    def test_return_404_if_user_doesnt_belong_to_the_game(self):
        new_user = User.objects.create_user(
            username='new_username',
            password='password',
            email='new_a@a.com'
        )
        new_game = Game.objects.create(name='new game', creator=new_user)
        Player.objects.create(user=new_user, current_game=new_game)
        http_authorization = build_http_auth_header('new_username', 'password')

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = http_authorization,
        )

        self.assertEqual(response.status_code, 404)

    def test_return_forbidden_if_player_doesnt_have_enough_money(self):
        self.player.cash = 0
        self.player.save()

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )

        self.assertEqual(response.status_code, 403)

    def test_player_buy_team_if_has_enough_money(self):
        self.player.cash = 1000
        self.player.save()
        self.assertFalse(GameTeam.objects.all())

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )
        player = Player.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(GameTeam.objects.all())
        game_team = GameTeam.objects.all()[0]
        self.assertEqual(game_team.player, player)
        self.assertEqual(player.cash, 1000 - game_team.team.salary)

    def test_return_forbidden_buying_other_player_team_if_hasnt_enough_money(self):
        cash = self.team.salary + 1
        self.player.cash = cash
        self.player.save()
        new_user = User.objects.create()
        new_player = Player.objects.create(user=new_user, current_game=self.game)
        GameTeam.objects.create(player=new_player, team=self.team)

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )
        player = Player.objects.get(user=self.user)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(GameTeam.objects.count(), 1)
        self.assertEqual(player.cash, cash)

    def test_return_forbidden_buying_other_player_team_if_hasnt_enough_money_and_team_was_bought_more_than_one_time(self):
        cash = self.team.salary + self.team.contract_cost + 1
        self.player.cash = cash
        self.player.save()
        new_user = User.objects.create()
        new_player = Player.objects.create(user=new_user, current_game=self.game)
        game_team = GameTeam.objects.create(player=new_player, team=self.team)
        game_team.times_bought = 2
        game_team.save()

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )
        player = Player.objects.get(user=self.user)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(GameTeam.objects.count(), 1)
        self.assertEqual(player.cash, cash)

    @patch('random.choice', Mock(return_value=False))
    def test_return_forbidden_buying_other_player_team_if_dice_doesnt_return_true(self):
        cash = self.team.salary + self.team.contract_cost + 1
        self.player.cash = cash
        self.player.save()
        new_user = User.objects.create()
        new_player = Player.objects.create(user=new_user, current_game=self.game)
        GameTeam.objects.create(player=new_player, team=self.team)

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )
        player = Player.objects.get(user=self.user)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(GameTeam.objects.count(), 1)
        self.assertEqual(player.cash, cash)

    @patch('random.choice', Mock(return_value=True))
    def test_return_success_buying_other_player_team_if_dice_return_true(self):
        cash = self.team.salary + self.team.contract_cost + 1
        self.player.cash = cash
        self.player.save()
        new_user = User.objects.create()
        new_player = Player.objects.create(user=new_user, current_game=self.game)
        game_team = GameTeam.objects.create(player=new_player, team=self.team)
        purchase_price = game_team.purchase_price

        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':self.team.uuid}),
            {'game_uuid':self.game.uuid},
            content_type='application/json',
            HTTP_AUTHORIZATION = self.http_authorization,
        )
        player = Player.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(GameTeam.objects.count(), 1)
        game_team = GameTeam.objects.all()[0]
        self.assertEqual(game_team.player, player)
        self.assertEqual(game_team.times_bought, 2)
        self.assertEqual(player.cash, cash - purchase_price)
