from django.conf.urls.defaults import *

from utils.shortcuts import route

urlpatterns = patterns('project_management.views',

    route(r'new/(?P<game_uuid>[\w-]+)/$', GET='get_new_project', name='get_project'),
    route(r'info/(?P<proj_uuid>[\w-]+)/$', GET='get_info', name='project_info')

)
