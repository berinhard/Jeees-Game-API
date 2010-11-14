# -*- encoding:utf-8 -*-
import random

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from game_config.decorators import user_auth
from game_config.models import Game, Player
from project_management.models import Project


@user_auth
def get_new_project(request, game_uuid):
    game = get_object_or_404(Game, uuid=game_uuid)
    player = get_object_or_404(Player, current_game=game, user=request.user)
    if player.project:
        return HttpResponseForbidden('o jogador já tem um projeto')

    current_game_projects = [
        player.project for player in Player.objects.filter(current_game=game)
    ]
    projects = [
        proj for proj in Project.objects.all() if not proj in current_game_projects
    ]

    player.project = random.choice(projects)
    player.save()

    return HttpResponse()
