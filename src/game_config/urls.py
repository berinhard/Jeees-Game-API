from django.conf.urls.defaults import *

from shortcuts import route

urlpatterns = patterns('game_config.views',

    route(r'^$', POST='create_game', name='create_game')

)