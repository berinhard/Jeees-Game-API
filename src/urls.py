from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from demoapp.handlers import DemoHandler
from piston.resource import Resource

class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

demo_handler = CsrfExemptResource(DemoHandler)

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/$', demo_handler),
    (r'^api/(?P<object_id>\d+)/$', demo_handler),
)
