from django.http import HttpResponse, HttpRequest

from .auth import Register, Login, JwtToken
from ..constants.constants import Ros_CONST
from .portal import User_Portal_Req


def facebook_login(request: HttpRequest):
    resp = Login.facebook_login(request.POST.get(Ros_CONST.LOGIN_REGIS.FACEBOOK_ACCESS_ID, None),
                                request.POST.get(Ros_CONST.Users.EMAIL, None),
                                request.POST.get(Ros_CONST.LOGIN_REGIS.DEVICE_ID, ""),
                                request.POST.get(Ros_CONST.LOGIN_REGIS.DEVICE_TYPE, ""))
    return HttpResponse(resp)


def rostrus_login(request: HttpRequest):
    resp = Login.rostrus_login(request.POST.get(Ros_CONST.Users.EMAIL, None),
                               request.POST.get(Ros_CONST.Users.PASSWORD, None),
                               request.POST.get(Ros_CONST.LOGIN_REGIS.DEVICE_ID, "Not Filled"),
                               request.POST.get(Ros_CONST.LOGIN_REGIS.DEVICE_TYPE, "Not Filled"))
    return HttpResponse(resp)


def test(request: HttpRequest):
    token = JwtToken()
    return HttpResponse(token.generate_token(5, 2, 321213, 321123))


def db_test(request: HttpRequest):
    get_data = JwtToken.verify_token(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJpaXMiOiJhcGkucm9zdHJ1cy5jb20iLCJpYXQiOjE0OTY1NjgzNzYuODc5MDY4OSwidXNlcl9pZCI6MTcsInBvcnRhbF9pZCI6MTQsImRldmljZV9pZCI6ImV4YW1wbGVfZGV2aWNlX3R5cGUiLCJkZXZpY2VfdHlwZSI6ImV4YW1wbGVfZGV2aWNlX2lkIn0.FWXtHihVy1Ri85NZJJtlm5gk7V10QH9qpRA3ZkhRzBXMtM0fQ61mdU614JSvMVfS")
    print(get_data)
    return HttpResponse("  SSS  ")


def register(request: HttpResponse):
    return HttpResponse(Register.register(request.POST[Ros_CONST.Portal.NAME], request.POST[Ros_CONST.Users.PASSWORD],
                                          request.POST[Ros_CONST.Users.FIRST_NAME],
                                          request.POST[Ros_CONST.Users.LAST_NAME],
                                          request.POST[Ros_CONST.Users.EMAIL], request.POST[Ros_CONST.Portal.PIC_URL],
                                          request.POST[Ros_CONST.Users.GENDER], request.POST[Ros_CONST.Users.DOB]))


def update_profile_pic_url(request: HttpRequest):
    return HttpResponse(
        User_Portal_Req.update_portal_prof_pic(request._PORTAL_ID, request.POST[Ros_CONST.Portal.PIC_URL]))


def del_profile_pic(request: HttpRequest):
    return HttpResponse(User_Portal_Req.delete_portal_prof_pic(request._PORTAL_ID))


def get_portal_prof_img_upload_auth(request: HttpRequest):
    return HttpResponse(User_Portal_Req.get_gcp_img_upload_auth(request._USER_ID, request._PORTAL_ID,
                                                                request.POST[Ros_CONST.Users.EMAIL]))
