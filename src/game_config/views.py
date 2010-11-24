# -*- encoding:utf-8 -*-
import json
import random

from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from game_config.models import Player, Game
from game_config.decorators import user_auth
from utils.decorators import unpack_data

@user_auth
@unpack_data
@never_cache
def create_game(request):
    post_data = request.post_data
    if not 'game_name' in post_data:
        return HttpResponseBadRequest(u'o campo game_name é obrigatóri')

    user = request.user
    try:
        user.get_profile()
        return HttpResponseForbidden(u'esse usuário já está em um jogo')
    except ObjectDoesNotExist:
        pass

    game = Game.objects.create(name=post_data['game_name'], creator=user)
    player = Player.objects.create(user=user, current_game=game)

    content = {
        'game': game.to_dict(),
        'game_info_uri':'/game/%s/' % game.uuid,
        'delete_game_uri':'/game/%s/' % game.uuid,
        'get_project_uri':'/project/new/%s' % game.uuid,
    }
    content = json.dumps(content)

    return HttpResponse(content)

@never_cache
def all_games(request):
    content = [__game_info_dict(game) for game in Game.objects.all()]
    content = json.dumps(content)
    return HttpResponse(content)

@user_auth
@never_cache
def leave_or_delete_game(request, uuid):
    game = get_object_or_404(Game, uuid=uuid)
    user = request.user
    if game.creator == user:
        game.delete()
    else:
        player = get_object_or_404(Player, user=user, current_game=game)
        player.delete()
    return HttpResponse('OK')

@user_auth
@never_cache
def join_game(request, uuid):
    game = get_object_or_404(Game, uuid=uuid)

    user = request.user
    try:
        user.get_profile()
        return HttpResponseForbidden('o usuário já está em um jogo')
    except ObjectDoesNotExist:
        pass

    Player.objects.create(user=user, current_game=game)
    content = {
        'game': game.to_dict(),
        'game_info_uri':'/game/%s/' % game.uuid,
        'leave_game_uri':'/game/%s/' % game.uuid,
        'get_project_uri':'/project/new/%s' % game.uuid,
    }
    content = json.dumps(content)

    return HttpResponse(content)

@never_cache
def game_info(request, uuid):
    game = get_object_or_404(Game, uuid=uuid)
    content = json.dumps(__game_info_dict(game))
    return HttpResponse(content)

def __game_info_dict(game):
    players = [
        {'uuid':player.uuid, 'username':player.user.username}
        for player in Player.objects.filter(current_game=game)
    ]

    content = {
        'game_info_uri':'/game/%s/' % game.uuid,
        'game':game.to_dict(),
        'players':players,
    }

    return content
