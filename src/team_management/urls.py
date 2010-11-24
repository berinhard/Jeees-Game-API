from django.conf.urls.defaults import *

from utils.shortcuts import route

urlpatterns = patterns('team_management.views',

    route(r'^$', GET='all_teams', name='root'),
    route(r'(?P<team_uuid>[\w-]+)/$', GET='team_info', POST='buy_team', name='single_team'),

)
