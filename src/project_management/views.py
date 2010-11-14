# -*- encoding:utf-8 -*-
import random
import json

from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from game_config.decorators import user_auth
from game_config.models import Game, Player
from project_management.models import Project


@user_auth
@never_cache
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

    project = random.choice(projects)
    player.project = project
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
