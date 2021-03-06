from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'game/', include('game_config.urls', namespace='game_config')),
    (r'team/', include('team_management.urls', namespace='teams')),
    (r'project/', include('project_management.urls', namespace='projects')),
)
