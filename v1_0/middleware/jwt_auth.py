import json
from django.http import HttpRequest

from ..src.user_portal.auth import JwtToken
from ..src.constants.constants import Ros_CONST


class Jwt_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):

        # TODO: Change for production
        excluded_views = ["aws_s3_img_upload", "db_test", "facebook_login", "register", "rostrus_login", "test"]
                        #[i[0] for i in inspect.getmembers(views, inspect.isfunction)][0:6]

        if excluded_views.__contains__(view_func.__name__):
            return None

        if request.method == "GET":
            data = JwtToken.verify_token(request.GET.get(Ros_CONST.LOGIN_REGIS.JWT_TOKEN))
            if data:
                request._USER_ID = data[Ros_CONST.Users.USER_ID]
                request._PORTAL_ID = data[Ros_CONST.Portal.ID]
            else:
                return json.dumps({"ERROR": "JWT Token not valid"})

        elif request.method == "POST":

            data = JwtToken.verify_token(request.POST.get(Ros_CONST.LOGIN_REGIS.JWT_TOKEN))
            print(data)
            if data:

                request._USER_ID = data[Ros_CONST.Users.USER_ID]
                request._PORTAL_ID = data[Ros_CONST.Portal.ID]

            else:
                return json.dumps({"ERROR": "JWT Token not valid"})

        return None
