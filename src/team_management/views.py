# -*- encoding:utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from game_config.decorators import user_auth
from game_config.models import Game, Player
from utils.decorators import unpack_data
from team_management.models import Team

@user_auth
@unpack_data
def buy_team(request, team_uuid):
    if not 'game_uuid' in request.post_data:
        return HttpResponseBadRequest('faltando o uuid do jogo no JSON')
    game_uuid = request.post_data['game_uuid']

    team = get_object_or_404(Team, uuid=team_uuid)
    game = get_object_or_404(Game, uuid=game_uuid)
    player = get_object_or_404(Player, user=request.user, current_game=game)

    if player.cash < team.salary:
        return HttpResponseForbidden('o jogador não tem dinheiro suficiente')

    return HttpResponse()
