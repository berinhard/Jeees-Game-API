from django.conf.urls.defaults import *

from utils.shortcuts import route

urlpatterns = patterns('team_management.views',

    route(r'(?P<team_uuid>[\w-]+)/$', POST='buy_team', name='single_team'),

)
