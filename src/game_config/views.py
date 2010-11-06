import json
import random

from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from game_config.models import Player, Game
from game_config.decorators import user_auth
from utils.decorators import unpack_data

@user_auth
@unpack_data
@never_cache
def create_game(request):
    post_data = request.post_data
    if not 'game_name' in post_data:
        return HttpResponseBadRequest()

    user = request.user
    if Player.objects.filter(user=user):
        return HttpResponseForbidden()

    game = Game.objects.create(name=post_data['game_name'])
    player = Player.objects.create(user=user, current_game=game)

    content = {
        'game': game.to_dict(),
        'delete_uri':'/%s/%s/' % (game.uuid, game.admin_token)
    }
    content = json.dumps(content)

    return HttpResponse(content)

@never_cache
def delete_game(request, uuid, admin_token):
    game = get_object_or_404(Game, uuid=uuid, admin_token=admin_token)
    game.delete()
    return HttpResponse()

@user_auth
@never_cache
def join_game(request, uuid):
    game = get_object_or_404(Game, uuid=uuid)

    user = request.user
    if Player.objects.filter(user=user):
        return HttpResponseForbidden()

    Player.objects.create(user=user, current_game=game)
    content = {
        'game': game.to_dict(),
    }
    content = json.dumps(content)

    return HttpResponse(content)

@never_cache
def game_info(request, uuid):
    game = get_object_or_404(Game, uuid=uuid)
    players = [
        {'uuid':player.uuid, 'username':player.user.username}
        for player in Player.objects.filter(current_game=game)
    ]

    content = {
        'game':game.to_dict(),
        'players':players,
    }
    content = json.dumps(content)

    return HttpResponse(content)
