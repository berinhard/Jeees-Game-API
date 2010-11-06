# -*- encoding:utf-8 -*-
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse

def user_auth(view):
    '''
    Decorator para autenticar o usuário
    Baseado no seguinte snippet
    http://djangosnippets.org/snippets/1720/
    '''
    def f(request, *args, **kwargs):
        username, password = __get_header_authorization(request)

        user = authenticate(username=username, password=password)
        if user:
            request.user = user
            response = view(request, *args, **kwargs)
        else:
            response = HttpResponse('username e senha incorretos', status=401)
            response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.JEEES_REALM

        return response

    return f


def __get_header_authorization(request):
    username = None
    password = None

    header = request.META.get('HTTP_AUTHORIZATION', None)
    if header:
        splitted_header = header.split()
        auth_string = splitted_header[1].decode('base64')
        username, password = auth_string.split(':')

    return username, password

