import json
import time

from .auth import Google_Cloud_Manager

from ...models import Portals


class User_Portal_Req:

    @staticmethod
    def update_portal_prof_pic(portal_id, img_url):

        cur_portal = Portals.objects.get(portal_id=portal_id)
        cur_portal.portal_profile_pic_url = img_url
        cur_portal.save()

        return json.dumps({"successful": True})

    @staticmethod
    def delete_portal_prof_pic(portal_id):

        cur_portal = Portals.objects.get(portal_id=portal_id)
        cur_portal.portal_profile_pic_url = None
        cur_portal.save()

        return json.dumps({"successful": True})

    @staticmethod
    def get_gcp_img_upload_auth(user_id, portal_id, email):

        token, uid = Google_Cloud_Manager.get_gcp_token(user_id, portal_id, email)

        file_name = uid[0:30] + str(int(time.time())) + "img_portprof"

        return json.dumps({"gcloud_token": token, "file_name": file_name})


