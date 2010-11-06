import json

from django.http import HttpResponseBadRequest

def unpack_data(view):

    def f(request, *args, **kwargs):
        post_data = {}
        try:
            post_data = json.loads(request.raw_post_data.replace("'", '"'))
        except ValueError:
            return HttpResponseBadRequest('json mal formatado')

        request.post_data = post_data
        return view(request, *args, **kwargs)

    f.__name__ = view.__name__
    f.__doc__ = view.__doc__
    return f
