from django.http import HttpRequest
from django.http import HttpResponse

from .reactions import Reactions_Reg
from ..rostrus import Ros_CONST as Rc


def post_reaction_update(request: HttpRequest):
    return HttpResponse(Reactions_Reg.post_reaction_update(request._PORTAL_ID, request.POST[Rc.Posts.ID],
                                                           request.POST[Rc.Posts.LIKED_OR_DISLIKED]))


def comm_reaction_update(request: HttpRequest):
    return HttpResponse(Reactions_Reg.comm_reaction_update(request._PORTAL_ID, request.POST[Rc.Comments.ID],
                                                           request.POST[Rc.Comments.LIKE_OR_DISLIKE]))
