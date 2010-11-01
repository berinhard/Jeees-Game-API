from django.conf.urls.defaults import *

from utils.shortcuts import route

urlpatterns = patterns('game_config.views',

    route(r'^$', POST='create_game', name='create_game'),
    route(r'(?P<uuid>[\w-]+)/$', DELETE='delete_game', name='delete_game')

)
