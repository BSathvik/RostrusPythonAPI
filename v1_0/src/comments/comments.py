import json
import time
from django.db.models import F
from django.db import connection

from ..rostrus import Ros_CONST as RC, Rostrus

from ...models import Comments
from ...models import Posts


class Comments_Req:
    @staticmethod
    def insert_comment(portal_id, post_id, comment_body, comment_parent_id):
        time_this = int(time.time())

        insert_comment_id = -1

        if int(comment_parent_id) == -1:
            new_comment = Comments(post_id=post_id, comment_portal_id=portal_id, comment_body=comment_body,
                                   comment_datetime=time_this)
            new_comment.save()
            insert_comment_id = new_comment.pk

            update_post = Posts.objects.get(post_id=post_id)
            update_post.num_root_comments = F('num_root_comments') + 1
            update_post.save()

        else:

            get_comment = Comments.objects.get(comment_id=comment_parent_id)
            comment_level = get_comment.comment_level + 1

            new_comment = Comments(post_id=post_id, comment_portal_id=portal_id, comment_body=comment_body,
                                   comment_datetime=time_this, comment_level=comment_level, comment_parent_id=comment_parent_id)
            new_comment.save()
            insert_comment_id = new_comment.pk

            num_child_comm = Comments.objects.get(comment_id=comment_parent_id)
            num_child_comm.num_child_comments = F('num_child_comments') + 1
            num_child_comm.save()

        return {"successful": True, RC.Comments.PUB_TIME: time_this, RC.Comments.ID: insert_comment_id}

    @staticmethod
    def get_post_comments(portal_id, post_id, limit=10, offset=0):

        cursor = connection.cursor()

        db_mapping = [RC.Comments.ID, RC.Comments.POST_ID, RC.Comments.NUM_REPLIES, RC.Comments.PORTAL_ID, RC.Portal.NAME,
                      RC.Comments.TEXT_BODY, RC.Portal.PIC_URL, RC.Comments.LIKES, RC.Comments.DISLIKES, RC.Comments.PARENT_ID,
                      RC.Comments.LEVEL, RC.Comments.PUB_TIME,
                      RC.Comments.LIKE_OR_DISLIKE,
                      portal_id, post_id, limit, offset]

        sql = '''SELECT com.comment_id AS %s, com.post_id AS %s, com.num_child_comments AS %s, com.comment_portal_id AS %s, port.portal_name AS %s, com.comment_body AS %s, port.portal_profile_pic_url AS %s,
                        com.comment_likes AS %s, com.comment_dislikes AS %s, com.comment_parent_id AS %s, com.comment_level AS %s, com.comment_datetime AS %s, com_ld.like_or_dislike AS %s
                                        FROM portals port, comments com
                                        LEFT JOIN comments_likes_dislikes com_ld ON com.comment_id = com_ld.comment_id AND com_ld.portal_id = %s
                                        WHERE com.comment_portal_id = port.portal_id
                                        AND com.post_id = %s AND com.comment_parent_id IS NULL
                                        LIMIT %s OFFSET %s'''

        cursor.execute(sql, db_mapping)

        resp_data = Comments_Req.__comm_data(cursor, portal_id, True)

        return resp_data

    @staticmethod
    def get_comm_comments(portal_id, comm_parent_id, post_id, limit=10, offset=0):

        cursor = connection.cursor()

        db_mapping = [RC.Comments.ID, RC.Comments.POST_ID, RC.Comments.NUM_REPLIES, RC.Comments.PORTAL_ID,
                      RC.Portal.NAME, RC.Comments.TEXT_BODY, RC.Portal.PIC_URL, RC.Comments.LIKES,
                      RC.Comments.DISLIKES, RC.Comments.PARENT_ID, RC.Comments.LEVEL, RC.Comments.PUB_TIME,
                      RC.Comments.LIKE_OR_DISLIKE, portal_id, post_id, comm_parent_id, limit, offset]

        sql = '''SELECT com.comment_id AS %s, com.post_id AS %s, com.num_child_comments AS %s, com.comment_portal_id AS %s, port.portal_name AS %s, com.comment_body AS %s, port.portal_profile_pic_url AS %s,
                        com.comment_likes AS %s, com.comment_dislikes AS %s, com.comment_parent_id AS %s, com.comment_level AS %s, com.comment_datetime AS %s, com_ld.like_or_dislike AS %s
                                        FROM portals port, comments com
                                        LEFT JOIN comments_likes_dislikes com_ld ON com.comment_id = com_ld.comment_id AND com_ld.portal_id = %s
                                        WHERE com.comment_portal_id = port.portal_id
                                        AND com.post_id = %s AND com.comment_parent_id = %s
                                        LIMIT %s OFFSET %s'''
        cursor.execute(sql, db_mapping)

        resp_data = Comments_Req.__comm_data(cursor, portal_id, False)

        return resp_data

    @staticmethod
    def __comm_data(cursor, portal_id, isRootComments=False):

        db_data = Rostrus.dict_fetchall(cursor)

        if db_data is False:
            return {RC.Comments.REPLIES_AVAIL: False, "len": 0, "data": []}


        for comment in db_data:

            comment[RC.Comments.REPLIES] = []

            if isRootComments and comment[RC.Comments.NUM_REPLIES] > 0:
                comment[RC.Comments.REPLIES] += Comments_Req.get_comm_comments(portal_id=portal_id, comm_parent_id=comment[RC.Comments.ID], post_id=comment[RC.Comments.POST_ID])["data"]

            if comment[RC.Comments.LIKE_OR_DISLIKE] is None:
                comment[RC.Comments.LIKE_OR_DISLIKE] = 0

            if comment[RC.Comments.PARENT_ID] is None:
                comment[RC.Comments.PARENT_ID] = -1

            add_comm_data = {RC.Comments.REPLIES_AVAIL: True, RC.Comments.POST_ID: comment[RC.Comments.POST_ID]}
            comment.update(add_comm_data)


        resp_data = {RC.Comments.REPLIES_AVAIL: True, "len": db_data.__len__(), "data": db_data}

        return resp_data

    @staticmethod
    def delete_comment(portal_id, comment_id):

        try:
            print("Exists!")
            get_comm = Comments.objects.get(comment_id=comment_id)
            if get_comm.comment_portal_id == portal_id:
                get_comm.delete()
            else:
                return {"successful": False, "error": "Cannot delete the comment of another portal"}
        except Comments.DoesNotExist:
            print("Does not exists")

        return {"successful": True}
