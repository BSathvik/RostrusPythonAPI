import json
import facebook
import bcrypt
from django.db import connection
from datetime import datetime
from configparser import ConfigParser
import jwt
import time

import hashlib

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from django.conf import settings

from ..rostrus import Ros_CONST, Rostrus

from v1_0.models import Users
from v1_0.models import Portals
from v1_0.models import Portals_Users


class Login:
    @staticmethod
    def rostrus_login(email, password, device_type, device_id):

        user_exists = Users.objects.filter(user_email=email)

        if user_exists.count() == 0:
            return json.dumps({Ros_CONST.Users.USER_ID: Ros_CONST.LOGIN_REGIS.LOGIN_FAIL})

        db_password = user_exists[0].user_password

        if not bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
            return json.dumps({Ros_CONST.Users.USER_ID: Ros_CONST.LOGIN_REGIS.LOGIN_FAIL})

        resp = json.dumps(Login.get_data(email, device_type, device_id))

        return resp

    @staticmethod
    def facebook_login(access_id, email, device_type, device_id):

        fb = facebook.GraphAPI(access_token=access_id)

        try:
            profile = fb.get_object('me', **{'fields': 'email'})
            fb_email = profile.get('email')

            if fb_email == email:
                return json.dumps(Login.get_data(fb_email, device_type, device_id))  # User Data

        except facebook.GraphAPIError:

            return json.dumps({"ERROR": "The Facebook Access ID is invalid",
                               Ros_CONST.Users.USER_ID: Ros_CONST.LOGIN_REGIS.LOGIN_FAIL})

        return json.dumps({"ERROR": "Facebook login server error"})

    @staticmethod
    def get_data(email, device_type, device_id):

        cursor = connection.cursor()
        insert_data = [Ros_CONST.Users.USER_ID, Ros_CONST.Portal.ID, Ros_CONST.Portal.NAME,
                       Ros_CONST.Users.FIRST_NAME, Ros_CONST.Users.LAST_NAME, Ros_CONST.Users.EMAIL,
                       Ros_CONST.Users.LEVEL,
                       Ros_CONST.Portal.PIC_URL, Ros_CONST.Portal.USER_PORTAL_REL, email]

        cursor.execute('''SELECT u.user_id AS %s, port.portal_id AS %s, port.portal_name AS %s, u.user_firstname AS %s, u.user_lastname AS %s,
                          u.user_email AS %s, u.user_level AS %s, port.portal_profile_pic_url AS %s, pu.portal_relation_type AS %s
                                           FROM users u
                                           JOIN portals_users pu ON u.user_id = pu.user_id AND pu.portal_relation_type = '0'
                                           JOIN portals port ON port.portal_id = pu.portal_id
                                           WHERE u.user_email = %s;''', insert_data)

        db_data = Rostrus.dict_fetchall(cursor)[0]

        jwt_token = JwtToken.generate_token(db_data[Ros_CONST.Users.USER_ID], db_data[Ros_CONST.Portal.ID], device_type,
                                            device_id)

        add_resp = {Ros_CONST.LOGIN_REGIS.JWT_TOKEN: jwt_token, Ros_CONST.Error.ERROR: True,
                    Ros_CONST.Error.POST_VARIABLE_NS: 0}

        db_data.update(add_resp)

        return db_data


class Register:
    @staticmethod
    def register(username, password, f_name, l_name, user_email, profile_pic_url, user_gender,
                 user_date_of_birth):

        if profile_pic_url is None or profile_pic_url == "":
            profile_pic_url = "http://i2.cdn.cnn.com/cnnnext/dam/assets/161107120239-01-trump-parry-super-169.jpg"

        user_exist = Users.objects.filter(user_email=user_email)

        if user_exist.count() > 0:
            return json.dumps({Ros_CONST.LOGIN_REGIS.REGIS_ERROR: Ros_CONST.Users.EMAIL})

        portal_name_exist = Portals.objects.filter(portal_name=username)

        if portal_name_exist.count() > 0:
            return json.dumps({Ros_CONST.LOGIN_REGIS.REGIS_ERROR: Ros_CONST.Users.USERNAME})

        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        __time = int(datetime.utcnow().timestamp())

        new_user = Users(user_firstname=f_name, user_lastname=l_name, user_email=user_email, user_gender=user_gender,
                         user_password=hash_password,
                         registration_time=__time, user_DOB=user_date_of_birth)
        new_user.save()

        new_portal = Portals(portal_name=username, portal_profile_pic_url=profile_pic_url, time_log=__time)
        new_portal.save()


        portal_user_rel = Portals_Users(portal_id=new_portal.pk, user_id=new_user.pk, portal_relation_type=0)
        portal_user_rel.save()

        return json.dumps({Ros_CONST.LOGIN_REGIS.REGIS_ERROR: Ros_CONST.LOGIN_REGIS.REGIS_SUCCESS})


class JwtToken:

    @staticmethod
    def generate_token(user_id, portal_id, device_type="Null", device_id="Null"):

        parser = ConfigParser()
        parser.read(Rostrus.get_config_file_path())

        secret = parser.get('jwt', 'secret')

        payload = {"iis": "api.rostrus.com", "iat": time.time(), "user_id": user_id, "portal_id": portal_id,
                   "device_id": device_id, "device_type": device_type}

        token = jwt.encode(payload, secret, algorithm='HS384').decode("utf-8")

        return token

    @staticmethod
    def verify_token(token):

        parser = ConfigParser()
        parser.read(Rostrus.get_config_file_path())
        secret = parser.get('jwt', 'secret')

        try:
            payload = jwt.decode(token, secret, algorithms=['HS384'])
            user_id = payload.get("user_id")
            portal_id = payload.get("portal_id")

            return {"user_id": user_id, "portal_id": portal_id}

        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError, jwt.exceptions.InvalidKeyError):
            return False


class Google_Cloud_Manager:
    @staticmethod
    def get_gcp_token(user_id, portal_id, email):
        hashed_email = hashlib.sha224(email.encode("utf-8")).hexdigest()
        uid = str(user_id) + "_" + str(portal_id) + "_" + hashed_email

        custom_token = auth.create_custom_token(uid=uid).decode("utf-8")

        return [custom_token, uid]

    @staticmethod
    def initialise_gcp():
        cred = credentials.Certificate(
            settings.BASE_DIR + "/v1_0/restricted/rostrus-529f3-firebase-adminsdk-9kk4u-fdfcddbf44.json")
        firebase_admin.initialize_app(cred)



