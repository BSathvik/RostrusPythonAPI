from datetime import datetime
import json
from django.db import connection
from ..rostrus import Rostrus
from ..rostrus import Ros_CONST

from ...models import Portals_Tags


class Tags_Req:
    @staticmethod
    def sub_to_tag(portal_id, tag_id):
        time = int(datetime.timestamp())
        check_portal_tag_rel = Portals_Tags.objects.filter(portal_id=portal_id, tag_id=tag_id)

        if check_portal_tag_rel.count() == 0:
            new_portal_tag_rel = Portals_Tags(portal_id=portal_id, tag_id=tag_id, time_log=time)
            new_portal_tag_rel.save()
            return {"successful": True}

    @staticmethod
    def unsub_to_tag(portal_id, tag_id):
        check_portal_tag_rel = Portals_Tags.objects.filter(portal_id=portal_id, tag_id=tag_id)

        if check_portal_tag_rel.count() > 0:
            Portals_Tags.objects.filter(portal_id=portal_id, tag_id=tag_id).delete()
            return {"successful": True}

    @staticmethod
    def get_portal_sub_tags(portal_id):
        cursor = connection.cursor()

        db_mapping = [Ros_CONST.Tags.TAGS, Ros_CONST.Tags.NAME, Ros_CONST.Tags.DESC, Ros_CONST.Tags.TIME, portal_id]
        sql = '''SELECT t.tag_id AS %s, t.tag_name AS %s, t.tag_desc AS %s, t.time_log AS %s
                                           FROM portals_tags port_tag
                                           INNER JOIN tags t ON t.tag_id = port_tag.tag_id
                                           WHERE port_tag.portal_id = %s'''

        cursor.execut(sql, db_mapping)
        tags_data = Rostrus.dict_fetchall(cursor)

        resp_data = []

        for tag in tags_data:
            tag[Ros_CONST.Tags.IS_SUBED] = True
            resp_data.append(tag)

        return resp_data

