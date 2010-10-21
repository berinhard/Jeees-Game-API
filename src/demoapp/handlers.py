import json

from piston.handler import BaseHandler
from piston.utils import rc

from demoapp.models import DemoModel

class DemoHandler(BaseHandler):
    allowed_methods = ('POST', 'GET', 'DELETE')
    model = DemoModel

    def read(self, request, object_id):
        return DemoModel.objects.get(id=object_id)

    def delete(self, request, object_id):
        obj = DemoModel.objects.get(id=object_id)
        obj.delete()
        return rc.DELETED

    def create(self, request):
        data = json.loads(request.raw_post_data)
        DemoModel.objects.create(
            email=data.get('email', ''),
            name=data.get('name', ''),
            birthday=data.get('birthday', None)
        )
        return rc.CREATED
