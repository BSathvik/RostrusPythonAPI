import json
from datetime import datetime
from django.db import connection

from ..rostrus import Rostrus
from ..constants.constants import Ros_CONST as Rc

from ...models import Posts
from ...models import Tags
from ...models import Posts_Tags



class Article:
    @staticmethod
    def insert_article(post_title, post_desc, post_author_id, tags, post_article, post_type=1):

        time = int(datetime.utcnow().timestamp())
        new_post = Posts(post_name=post_title, post_article=post_article, post_desc=post_desc,
                         post_author_portal_id=post_author_id, post_type=post_type, post_datetime=time)
        new_post.save()

        post_id = new_post.pk
        existing_tags = []

        if tags is not None:
            tags = json.loads(tags)
            tags = [tag.get("tag_name") for tag in tags]

            sql = "SELECT tag_id, tag_name FROM tags WHERE tag_name IN (%s)" % (','.join(['%s'] * len(tags)))

            cursor = connection.cursor()

            cursor.execute(sql, tags)
            tags_db = Rostrus.dict_fetchall(cursor)

            for tag_db in tags_db:
                tag_id_db = tag_db.get(Rc.Tags.ID)
                tag_name_db = tag_db.get(Rc.Tags.NAME)

                existing_tags.append(tag_name_db)
                new_posts_tags = Posts_Tags(post_id=post_id, tag_id=tag_id_db, time_log=time)
                new_posts_tags.save()

            insert_tags = set(tags).difference(existing_tags)

            for in_tag in insert_tags:
                new_tag = Tags(tag_name=in_tag, time_log=time)
                new_tag.save()
                cur_tag_id = new_tag.pk

                in_post_tags = Posts_Tags(post_id=post_id, tag_id=cur_tag_id, time_log=time)
                in_post_tags.save()


        return {"successful": "ok"}

    @staticmethod
    def __get_json_tags(db_tags: str, tags_subed_id: str):



        tags_ar = db_tags.split("$*~*$")
        subed_tag_id = tags_subed_id.split(",")

        tags_json_ar = []
        count = 0

        for tag in tags_ar:
            tag_data_t = tag.split("/-*-/")

            if tag_data_t.__len__() > 0 and subed_tag_id[count] == int(tag_data_t[0]):
                is_subed = True
                count += 1
            else:
                is_subed = False

            tags_json_ar.append({Rc.Tags.ID: tag_data_t[0], Rc.Tags.NAME: tag_data_t[1], Rc.Tags.DESC: tag_data_t[2],
                                 Rc.Tags.IS_SUBED: is_subed})

        return tags_json_ar

    @staticmethod
    def get_personalized_posts(portal_id):

        db_mapping = [Rc.Posts.ID, Rc.Posts.ARTICLE_TITLE, Rc.Posts.TYPE, Rc.Posts.ARTICLE_DESCRIPTION, Rc.Posts.ARTICLE_URL,
                      Rc.Posts.NUM_VIEWS, Rc.Posts.TOTAL_LIKES, Rc.Posts.NUM_LIKES, Rc.Posts.NUM_DISLIKES, Rc.Portal.ID, Rc.Portal.NAME,
                      Rc.Portal.PIC_URL, Rc.Posts.DATETIME, Rc.Posts.LIKED_OR_DISLIKED, Rc.Posts.NUM_ROOT_COMMENTS, Rc.Tags.TAGS,
                      "subed_tag_id", portal_id]

        sql = '''SELECT p.post_id AS %s, p.post_name AS %s, p.post_type AS %s, p.post_desc AS %s, p.post_article AS %s, p.num_views AS %s, p.post_total_likes AS %s,
                        p.post_likes AS %s, p.post_dislikes AS %s, p.post_author_portal_id AS %s, port.portal_name AS %s, port.portal_profile_pic_url AS %s,
                        p.post_datetime AS %s, ANY_VALUE(pld.like_or_dislike) AS %s, p.num_root_comments AS %s,
                        (SELECT GROUP_CONCAT(CONCAT_WS('/-*-/',pt.tag_id, tag.tag_name, tag.tag_desc) SEPARATOR '$*~*$') FROM posts_tags pt JOIN tags tag ON pt.tag_id = tag.tag_id
                        WHERE post_id = p.post_id) AS %s,
                        GROUP_CONCAT(t.tag_id SEPARATOR ',') AS %s

                    FROM portals_tags port_tag

                    JOIN tags t ON port_tag.tag_id = t.tag_id
                    JOIN posts_tags pt ON pt.tag_id = t.tag_id
                    JOIN posts p ON p.post_id = pt.post_id
                    LEFT JOIN portals port ON p.post_author_portal_id = port.portal_id
                    LEFT OUTER JOIN posts_likes_dislikes pld ON p.post_id = pld.post_id

                    WHERE port_tag.portal_id = %s
                    GROUP BY p.post_id;'''

        cursor = connection.cursor()
        cursor.execute(sql, db_mapping)

        resp_data = Article.__process_db_post_data(cursor)

        return resp_data


    @staticmethod
    def get_posts_sub_tag(portal_id, tag_id, limit=10):

        cursor = connection.cursor()

        db_mapping = [Rc.Posts.ID, Rc.Posts.ARTICLE_TITLE, Rc.Posts.TYPE, Rc.Posts.ARTICLE_DESCRIPTION, Rc.Posts.ARTICLE_URL,
                      Rc.Posts.NUM_VIEWS, Rc.Posts.TOTAL_LIKES, Rc.Posts.NUM_LIKES, Rc.Posts.NUM_DISLIKES, Rc.Portal.ID, Rc.Portal.NAME,
                      Rc.Portal.PIC_URL, Rc.Posts.DATETIME, Rc.Posts.LIKED_OR_DISLIKED, Rc.Posts.NUM_ROOT_COMMENTS, Rc.Tags.TAGS, portal_id,
                      "subed_tag_id", tag_id, limit]

        sql = '''SELECT p.post_id AS %s, p.post_name AS %s, p.post_type AS %s, p.post_desc AS %s, p.post_article AS %s, p.num_views AS %s, p.post_total_likes AS %s, p.post_likes AS %s,
                        p.post_dislikes AS %s, p.post_author_portal_id AS %s, port.portal_name AS %s, port.portal_profile_pic_url AS %s,p.post_datetime AS %s, ANY_VALUE(pld.like_or_dislike) AS %s,
                        p.num_root_comments AS %s,
                        GROUP_CONCAT(CONCAT_WS('/-*-/',t.tag_id, t.tag_name, t.tag_desc) SEPARATOR '$*~*$') AS %s,
                        GROUP_CONCAT(((SELECT tag_id FROM portals_tags WHERE portals_tags.tag_id = t.tag_id AND portals_tags.portal_id = %s )) SEPARATOR ',' ) AS %s

                     FROM posts_tags pts
                     RIGHT JOIN posts p ON p.post_id = pts.post_id
                     JOIN portals port ON p.post_author_portal_id = port.portal_id
                     LEFT JOIN posts_likes_dislikes pld ON p.post_id = pld.post_id
                     LEFT JOIN tags t ON pts.tag_id = t.tag_id
                     WHERE pts.post_id IN (SELECT post_id FROM posts_tags WHERE tag_id = %s)

                     GROUP BY p.post_id
                     LIMIT %s;'''

        cursor.execute(sql, db_mapping)

        resp_data = Article.__process_db_post_data(cursor)

        return resp_data

    @staticmethod
    def get_posts_sub_portal(portal_id, sub_portal_id, limit=10):

        cursor = connection.cursor()

        db_mapping = [Rc.Posts.ID, Rc.Posts.ARTICLE_TITLE, Rc.Posts.TYPE, Rc.Posts.ARTICLE_DESCRIPTION, Rc.Posts.ARTICLE_URL,
                      Rc.Posts.NUM_VIEWS, Rc.Posts.TOTAL_LIKES, Rc.Posts.NUM_LIKES, Rc.Posts.NUM_DISLIKES, Rc.Portal.ID, Rc.Portal.NAME,
                      Rc.Portal.PIC_URL, Rc.Posts.DATETIME, Rc.Posts.LIKED_OR_DISLIKED, Rc.Posts.NUM_ROOT_COMMENTS, Rc.Tags.TAGS, portal_id,
                      "subed_tag_id", sub_portal_id, limit]

        # TODO: sub_portal_id may be a problem

        sql = '''SELECT p.post_id AS %s, p.post_name AS %s, p.post_type AS %s, p.post_desc AS %s, p.post_article AS %s, p.num_views AS %s, p.post_total_likes AS %s, p.post_likes AS %s,
                        p.post_dislikes AS %s, p.post_author_portal_id AS %s, port.portal_name AS %s, port.portal_profile_pic_url AS %s,p.post_datetime AS %s, ANY_VALUE(pld.like_or_dislike) AS %s,
                        p.num_root_comments AS %s,
                        GROUP_CONCAT(CONCAT_WS('/-*-/',t.tag_id, t.tag_name, t.tag_desc) SEPARATOR '$*~*$') AS %s,
                        GROUP_CONCAT(((SELECT tag_id FROM portals_tags WHERE portals_tags.tag_id = t.tag_id AND portals_tags.portal_id = %s )) SEPARATOR ',' ) AS %s

                        FROM posts p

                        LEFT JOIN portals port ON p.post_author_portal_id = port.portal_id
                        LEFT JOIN posts_tags pt ON pt.post_id = p.post_id
                        LEFT JOIN tags t ON t.tag_id = pt.tag_id

                        LEFT OUTER JOIN posts_likes_dislikes pld ON p.post_id = pld.post_id

                        WHERE port.portal_id = %s
                        GROUP BY p.post_id
                        LIMIT %s;'''

        cursor.execute(sql, db_mapping)

        resp_data = Article.__process_db_post_data(cursor)

        return resp_data

    @staticmethod
    def get_single_post(portal_id, post_id):

        cursor = connection.cursor()

        db_mapping = [Rc.Posts.ID, Rc.Posts.ARTICLE_TITLE, Rc.Posts.TYPE, Rc.Posts.ARTICLE_DESCRIPTION, Rc.Posts.ARTICLE_URL,
                      Rc.Posts.NUM_VIEWS, Rc.Posts.TOTAL_LIKES, Rc.Posts.NUM_LIKES, Rc.Posts.NUM_DISLIKES, Rc.Portal.ID, Rc.Portal.NAME,
                      Rc.Portal.PIC_URL, Rc.Posts.DATETIME, Rc.Posts.LIKED_OR_DISLIKED, Rc.Posts.NUM_ROOT_COMMENTS, Rc.Tags.TAGS, portal_id,
                      "subed_tag_id", post_id]


        sql = '''SELECT p.post_id AS %s, p.post_name AS %s, p.post_type AS %s, p.post_desc AS %s, p.post_article AS %s, p.num_views AS %s, p.post_total_likes AS %s, p.post_likes AS %s,
                        p.post_dislikes AS %s, p.post_author_portal_id AS %s, port.portal_name AS %s, port.portal_profile_pic_url AS %s,p.post_datetime AS %s, ANY_VALUE(pld.like_or_dislike) AS %s,
                        p.num_root_comments AS %s,
                        GROUP_CONCAT(CONCAT_WS('/-*-/',t.tag_id, t.tag_name, t.tag_desc) SEPARATOR '$*~*$') AS %s,
                        GROUP_CONCAT(((SELECT tag_id FROM portals_tags WHERE portals_tags.tag_id = t.tag_id AND portals_tags.portal_id = %s )) SEPARATOR ',' ) AS %s

                        FROM posts p

                        LEFT JOIN portals port ON p.post_author_portal_id = port.portal_id
                        LEFT JOIN posts_tags pt ON pt.post_id = p.post_id
                        LEFT JOIN tags t ON t.tag_id = pt.tag_id

                        LEFT OUTER JOIN posts_likes_dislikes pld ON p.post_id = pld.post_id

                        WHERE p.post_id = %s;'''

        cursor.execute(sql, db_mapping)

        resp_data = Article.__process_db_post_data(cursor)

        return resp_data


    @staticmethod
    def __process_db_post_data(cursor):

        data = Rostrus.dict_fetchall(cursor)

        if data is False:
            return {"len": 0, "data": []}

        posts_data = []

        for post in data:

            if post[Rc.Posts.LIKED_OR_DISLIKED] is None:
                post[Rc.Posts.LIKED_OR_DISLIKED] = 0

            if post[Rc.Tags.TAGS] is None or post["subed_tag_id"] is None:
                tags_avail = False
                tags = "Nothing available"
            else:
                tags_avail = True
                tags = Article.__get_json_tags(post[Rc.Tags.TAGS], post["subed_tag_id"])

            if post[Rc.Portal.NAME] is not None or post[Rc.Portal.NAME] == "":
                title_is_present = True
            else:
                title_is_present = False

            post[Rc.Tags.TAGS_AVAILABLE] = tags_avail
            post[Rc.Tags.TAGS] = tags
            post[Rc.Posts.UPDATE_TITLE_PRESENT] = title_is_present

            posts_data.append(post)

        resp_data = {"data": posts_data, "len": posts_data.__len__()}

        return resp_data

    @staticmethod
    def update_post_article(portal_id, post_id, post_article):

        get_post = Posts.objects.get(post_id=post_id)

        if get_post.post_author_portal_id == portal_id:
            get_post.post_article = post_article
            get_post.save()
            return json.dumps({"successful": True})

        return {"successful": False, "error": "User is not authorized to modify the post"}


