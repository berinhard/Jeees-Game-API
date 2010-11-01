import json
import random

from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth import authenticate

from game_config.models import Player, Game

@never_cache
def create_game(request):
    post_data = {}
    try:
        #WTF!!!!
        post_data = json.loads(request.raw_post_data.replace("'", '"'))
        if not 'username' in post_data or not 'password' in post_data:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest()

    response = HttpResponse()
    user = authenticate(username=post_data['username'], password=post_data['password'])

    if not user:
        response.status_code = 401
        return response

    if not Player.objects.filter(user=user):
        game_name = post_data.get('game_name', str(random.randint(0, 1000)))
        game = Game.objects.create(name=game_name)
        player = Player.objects.create(user=user, current_game=game)
    else:
        response = HttpResponseForbidden()

    return response
