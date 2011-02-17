# -*- encoding:utf-8 -*-
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from game_config.models import Game, Player

def user_auth(view):
    '''
    Decorator para autenticar o usuário
    Baseado no seguinte snippet
    http://djangosnippets.org/snippets/1720/
    '''
    def f(request, *args, **kwargs):
        username, password = __get_header_authorization(request)

        user = authenticate(username=username, password=password)
        if user:
            request.user = user
            response = view(request, *args, **kwargs)
        else:
            response = HttpResponse('username e senha incorretos', status=401)
            response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.JEEES_REALM

        return response

    return f

def __get_header_authorization(request):
    username = None
    password = None

    header = request.META.get('HTTP_AUTHORIZATION', None)
    if header:
        splitted_header = header.split()
        auth_string = splitted_header[1].decode('base64')
        username, password = auth_string.split(':')

    return username, password

def get_player_and_game(view):

    def f(request, *args, **kwargs):
        try:
            game_uuid = kwargs['game_uuid']
        except KeyError:
            if not 'game_uuid' in request.post_data:
                return HttpResponseBadRequest('faltando o uuid do jogo no JSON')
            game_uuid = request.post_data['game_uuid']

        game = get_object_or_404(Game, uuid=game_uuid)
        player = get_object_or_404(Player, current_game=game, user=request.user)
        request.game = game
        request.player = player

        return view(request, *args, **kwargs)

    return f
