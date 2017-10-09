from django.http import HttpRequest
from django.http import HttpResponse

from .subscriptions import Subscriptions_Req
from ..rostrus import Ros_CONST as Rc


def sub_tag(request: HttpRequest):
    return HttpResponse(Subscriptions_Req.sub_tag(request._PORTAL_ID, request.POST[Rc.Tags.ID]))


def get_portal_sub_tags(request: HttpRequest):
    return HttpResponse(Subscriptions_Req.get_portal_sub_tags(request._PORTAL_ID))


def sub_portal(request: HttpRequest):
    return HttpResponse(Subscriptions_Req.portal_sub_portal(request._PORTAL_ID, request.POST[Rc.Portal.SUB_ID]))


def get_subed_portals(request: HttpRequest):
    return HttpResponse(Subscriptions_Req.get_portal_sub_portal(request._PORTAL_ID))
