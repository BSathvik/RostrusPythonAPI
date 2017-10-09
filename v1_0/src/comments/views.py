from django.http import HttpRequest
from django.http import HttpResponse

from ..rostrus import Ros_CONST as Rc, Rostrus
from .comments import Comments_Req


def write_comment(request: HttpRequest):
    data = Comments_Req.insert_comment(request._PORTAL_ID, request.POST[Rc.Comments.POST_ID],
                                       request.POST[Rc.Comments.TEXT_BODY],
                                       request.POST[Rc.Comments.PARENT_ID])
    data_resp = Rostrus.process_resp_data(data)
    return HttpResponse(data_resp)


def get_comments(request: HttpRequest):
    if Rc.Comments.PARENT_ID in request.POST and int(request.POST[Rc.Comments.PARENT_ID]) == -1:
        comm_data = Comments_Req.get_post_comments(request._PORTAL_ID, request.POST[Rc.Comments.POST_ID])
        comm_data_json = Rostrus.process_resp_data(comm_data)
        return HttpResponse(comm_data_json)
    else:
        data = Comments_Req.get_comm_comments(request._PORTAL_ID, request.POST[Rc.Comments.PARENT_ID],
                                              request.POST[Rc.Comments.POST_ID])
        resp_data_json = Rostrus.process_resp_data(data)
        return HttpResponse(resp_data_json)


def delete_comment(request: HttpRequest):
    data = Comments_Req.delete_comment(request._PORTAL_ID, request.POST[Rc.Comments.ID])
    data_resp = Rostrus.process_resp_data(data)
    return HttpResponse(data_resp)
