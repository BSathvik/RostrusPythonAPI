from django.http import HttpResponse
from django.http import HttpRequest


def index(request: HttpRequest):
    return HttpResponse("Shit is awesome!  " + str(request.GET['nothing']))

