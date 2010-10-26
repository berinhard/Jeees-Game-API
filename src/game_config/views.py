from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def create_game(request):
    print 'it works'
    return HttpResponse('foi')
