from django.conf.urls.defaults import *

from utils.shortcuts import route

urlpatterns = patterns('game_config.views',

    route(r'^$', POST='create_game', name='create_game'),
    route(r'(?P<uuid>[\w-]+)/(?P<admin_token>[\w-]+)/$', DELETE='delete_game', name='delete_game'),
    route(r'(?P<uuid>[\w-]+)/$', POST='join_game', GET='game_info', name='game_info'),

)
