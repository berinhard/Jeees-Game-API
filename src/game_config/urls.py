from django.conf.urls.defaults import *

from utils.shortcuts import route

urlpatterns = patterns('game_config.views',

    route(r'^$', GET='all_games', POST='create_game', name='root'),
    route(r'(?P<uuid>[\w-]+)/$', POST='join_game', GET='game_info', DELETE='leave_or_delete_game', name='game_info'),

)
