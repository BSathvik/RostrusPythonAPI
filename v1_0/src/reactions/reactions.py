import json
import time

from django.db import connection

from ...models import Posts_Likes_Dislikes, Comments_Likes_Dislikes


class Reactions_Reg:

    @staticmethod
    def post_reaction_update(portal_id, post_id, like_dislike):

        try:
            like_dislike_data = Posts_Likes_Dislikes.objects.get(post_id=post_id, portal_id=portal_id)

            if like_dislike == like_dislike_data.like_or_dislike:
                like_dislike_data.like_or_dislike = 0
            else:
                like_dislike_data.like_or_dislike = like_dislike
            like_dislike_data.save()

        except Posts_Likes_Dislikes.DoesNotExist:
            new_like_dislike = Posts_Likes_Dislikes(post_id=post_id, portal_id=portal_id, like_or_dislike=like_dislike, time_log=int(time.time()))
            new_like_dislike.save()
            return json.dumps({"successful": True})

        cursor = connection.cursor()
        db_map = [post_id]

        if like_dislike_data.like_or_dislike == -1 and like_dislike == 1:
            cursor.execute("UPDATE posts SET post_likes = post_likes + 1, post_dislikes = post_dislikes - 1, post_total_likes = post_total_likes + 2  WHERE post_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == -1 and like_dislike == -1:
            cursor.execute("UPDATE posts SET post_dislikes = post_dislikes - 1, post_total_likes = post_total_likes + 1  WHERE post_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 1 and like_dislike == 1:
            cursor.execute("UPDATE posts SET post_likes = post_likes - 1, post_total_likes = post_total_likes - 1  WHERE post_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 1 and like_dislike == -1:
            cursor.execute("UPDATE posts SET post_likes = post_likes - 1, post_dislikes = post_dislikes + 1, post_total_likes = post_total_likes - 2  WHERE post_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 0 and like_dislike == 1:
            cursor.execute("UPDATE posts SET post_likes = post_likes + 1, post_total_likes = post_total_likes + 1  WHERE post_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 0 and like_dislike == -1:
            cursor.execute("UPDATE posts SET post_dislikes = post_dislikes + 1, post_total_likes = post_total_likes - 1  WHERE post_id = %s", db_map)


        return json.dumps({"successful": True})

    @staticmethod
    def comm_reaction_update(portal_id, comment_id, like_dislike):

        try:
            like_dislike_data = Comments_Likes_Dislikes.objects.get(comment_id=comment_id, portal_id=portal_id)
            if like_dislike == like_dislike_data.like_or_dislike:
                like_dislike_data.like_or_dislike = 0
            else:
                like_dislike_data.like_or_dislike = like_dislike
            like_dislike_data.save()
        except Comments_Likes_Dislikes.DoesNotExist:
            new_like_dislike = Comments_Likes_Dislikes(comment_id=comment_id, portal_id=portal_id, like_or_dislike=like_dislike, time_log=int(time.time()))
            new_like_dislike.save()
            return json.dumps({"successful": True})


        cursor = connection.cursor()
        db_map = [comment_id]

        if like_dislike_data.like_or_dislike == -1 and like_dislike == 1:
            cursor.execute("UPDATE comments SET comment_likes = comment_likes + 1, comment_dislikes = comment_dislikes - 1, comment_total_likes = comment_total_likes + 2  WHERE comment_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == -1 and like_dislike == -1:
            cursor.execute("UPDATE comments SET comment_dislikes = comment_dislikes - 1, comment_total_likes = comment_total_likes + 1  WHERE comment_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 1 and like_dislike == 1:
            cursor.execute("UPDATE comments SET comment_likes = comment_likes - 1, comment_total_likes = comment_total_likes - 1  WHERE comment_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 1 and like_dislike == -1:
            cursor.execute("UPDATE comments SET comment_likes = comment_likes - 1, comment_dislikes = comment_dislikes + 1, comment_total_likes = comment_total_likes - 2  WHERE comment_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 0 and like_dislike == 1:
            cursor.execute("UPDATE comments SET comment_likes = comment_likes + 1, comment_total_likes = comment_total_likes + 1  WHERE comment_id = %s", db_map)
        elif like_dislike_data.like_or_dislike == 0 and like_dislike == -1:
            cursor.execute("UPDATE comments SET comment_dislikes = comment_dislikes + 1, comment_total_likes = comment_total_likes - 1  WHERE comment_id = %s", db_map)

        return json.dumps({"successful": True})

