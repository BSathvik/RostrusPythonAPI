import json
import time

from django.db import connection

from ...models import Portals_Tags, Portal_Sub_Portal
from ..constants.constants import Ros_CONST as Rc
from ..rostrus import Rostrus


class Subscriptions_Req:
    @staticmethod
    def sub_tag(portal_id, tag_id):

        check_portal_tag_rel = Portals_Tags.objects.filter(portal_id=portal_id, tag_id=tag_id)

        if check_portal_tag_rel.count() == 0:
            new_portal_tag_rel = Portals_Tags(portal_id=portal_id, tag_id=tag_id, time_log=int(time.time()))
            new_portal_tag_rel.save()
            return json.dumps({"successful": True, "action": "Subscribed"})
        elif check_portal_tag_rel.count() > 0:
            check_portal_tag_rel.delete()
            return json.dumps({"successful": True, "action": "Unsubscribed"})

        return json.dumps({"successful": False})

    @staticmethod
    def get_portal_sub_tags(portal_id):
        cursor = connection.cursor()

        db_mapping = [Rc.Tags.ID, Rc.Tags.NAME, Rc.Tags.DESC, Rc.Tags.TIME, portal_id]
        sql = '''SELECT t.tag_id AS %s, t.tag_name AS %s, t.tag_desc AS %s, t.time_log AS %s
                                           FROM portals_tags port_tag
                                           INNER JOIN tags t ON t.tag_id = port_tag.tag_id
                                           WHERE port_tag.portal_id = %s'''

        cursor.execute(sql, db_mapping)
        tags_data = Rostrus.dict_fetchall(cursor)

        if tags_data is False:
            return json.dumps({"len": 0, "data": []})

        tag_data = []

        for tag in tags_data:
            tag[Rc.Tags.IS_SUBED] = True
            tag_data.append(tag)

        resp_data = {"data": tags_data, "len": tags_data.__len__()}

        return json.dumps(resp_data)

    @staticmethod
    def portal_sub_portal(portal_id, sub_portal_id):

        check_portal_sub_rel = Portal_Sub_Portal.objects.filter(cur_portal_id=portal_id,
                                                                subed_to_portal_id=sub_portal_id)

        if check_portal_sub_rel.count() == 0:
            new_portal_sub_rel = Portal_Sub_Portal(cur_portal_id=portal_id, subed_to_portal_id=sub_portal_id,
                                                   time_log=int(time.time()))
            new_portal_sub_rel.save()
            return json.dumps({"successful": True, "action": "Subscribed"})
        elif check_portal_sub_rel.count() > 0:
            check_portal_sub_rel.delete()
            return json.dumps({"successful": True, "action": "Unsubscribed"})

        return json.dumps({"successful": False})

    @staticmethod
    def get_portal_sub_portal(portal_id):
        cursor = connection.cursor()

        db_mapping = [Rc.Portal.SUB_ID, Rc.Portal.SUB_NAME, Rc.Portal.SUB_DESC, Rc.Portal.SUB_PIC_URL,
                      Rc.Portal.SUB_TIME, portal_id]

        sql = '''SELECT psp.subed_to_portal_id AS %s, port_sub.portal_name AS %s, port_sub.portal_desc AS %s,
                        port_sub.portal_profile_pic_url AS %s, psp.time_log AS %s
                                           FROM portal_sub_portal psp
                                           JOIN portals port_sub ON port_sub.portal_id = psp.subed_to_portal_id
                                           WHERE psp.cur_portal_id  = %s'''
        cursor.execute(sql, db_mapping)

        db_data = Rostrus.dict_fetchall(cursor)

        if db_data is False:
            return json.dumps({"len": 0, "data": []})

        portal_data = []
        for portal in db_data:
            portal[Rc.Portal.SUB_IS_SUBED] = True
            portal_data.append(portal)

        resp_data = {"data": portal_data, "len": portal_data.__len__()}

        return json.dumps(resp_data)
