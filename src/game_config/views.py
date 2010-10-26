import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate

def create_game(request):
    post_data = {}
    try:
        #WTF!!!!
        post_data = json.loads(request.raw_post_data.replace("'", '"'))
        if not 'username' in post_data or not 'password' in post_data:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest()

    response = HttpResponse()
    user = authenticate(username=post_data['username'], password=post_data['password'])

    if not user:
        response.status_code = 401
        return response

    return response
