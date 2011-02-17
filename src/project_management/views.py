# -*- encoding:utf-8 -*-
import random
import json

from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from game_config.decorators import user_auth, get_player_and_game
from game_config.models import Game, Player
from team_management.models import GameTeam
from project_management.models import Project


@user_auth
@never_cache
@get_player_and_game
def get_new_project(request, game_uuid):
    game = request.game
    player = request.player

    if player.project:
        return HttpResponseForbidden('o jogador já tem um projeto')

    current_game_projects = [
        player.project for player in Player.objects.filter(current_game=game)
    ]
    projects = [
        proj for proj in Project.objects.all() if not proj in current_game_projects
    ]

    project = random.choice(projects)
    player.project = project
    player.cash = project.initial_cash
    player.save()

    content = json.dumps({'project_info_uri':'/project/info/%s' % project.uuid})

    return HttpResponse(content)

@never_cache
def get_info(request, proj_uuid):
    project = get_object_or_404(Project, uuid=proj_uuid)
    content = project.to_dict()
    content.update({'releases':
        [release.to_dict() for release in project.release_set.all()]
    })
    return HttpResponse(json.dumps(content))

@never_cache
@user_auth
@get_player_and_game
def work_pontuation(request, game_uuid):
    game = request.game
    player = request.player

    teams = [t for t in GameTeam.objects.all() if t.player == player]
    if not teams:
        return HttpResponseBadRequest('O jogador não possui time ainda')

    development_points = 0
    testing_points = 0

    for team in teams:
        if team.development:
            for i in range(team.team.development_points):
                development_points += random.randint(1, 6)
        else:
            for i in range(team.team.testing_points):
                testing_points += random.randint(1, 6)

    content = {
        'development_points':development_points,
        'testing_points':testing_points,
    }

    return HttpResponse(json.dumps(content))
