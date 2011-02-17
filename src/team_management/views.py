# -*- encoding:utf-8 -*-
import random
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from game_config.decorators import user_auth, get_player_and_game
from game_config.models import Game, Player
from utils.decorators import unpack_data
from team_management.models import Team, GameTeam

@user_auth
@unpack_data
@never_cache
@get_player_and_game
def buy_team(request, team_uuid):
    game = request.game
    player = request.player

    team = get_object_or_404(Team, uuid=team_uuid)

    oponent_game_team = GameTeam.objects.filter(
        team=team, player__current_game=game).exclude(player=player)

    if oponent_game_team:
        game_team = oponent_game_team[0]
        return __buy_oponent_team(game_team, player)
    else:
        return __team_first_purchase(team, player)

    if response.status_code != 200:
        return response

    return response

def __team_first_purchase(team, player):
    if player.cash < team.salary:
        return HttpResponseForbidden('o jogador não tem dinheiro suficiente')

    game_team = GameTeam.objects.create(player=player, team=team)
    content = json.dumps(game_team.to_dict())

    player.cash -= team.salary
    player.save()

    return HttpResponse(content)

def __buy_oponent_team(game_team, player):
    purchase_price = game_team.purchase_price
    if player.cash < purchase_price:
        return HttpResponseForbidden('o jogador não tem dinheiro suficiente')

    success = random.choice([True, False])
    if not success:
        return HttpResponseForbidden('não teve sorte ao tentar comprar')

    game_team.player = player
    game_team.times_bought += 1
    game_team.save()
    content = json.dumps(game_team.to_dict())

    player.cash -= purchase_price
    player.save()

    return HttpResponse(content)

@never_cache
def team_info(request, team_uuid, game_uuid=None):
    if game_uuid:
        team = get_object_or_404(GameTeam, player__current_game__uuid=game_uuid)
    team = get_object_or_404(Team, uuid=team_uuid)
    content = team.to_dict()
    content = json.dumps(content)
    return HttpResponse(content)

@never_cache
def all_teams(request):
    content = [team.to_dict() for team in Team.objects.all()]
    content = json.dumps(content)
    return HttpResponse(content)
