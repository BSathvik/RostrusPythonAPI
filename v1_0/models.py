from django.db import models


class Test(models.Model):
    class Meta:
        db_table = "test"

    number = models.IntegerField()
    txt = models.TextField()


class Users(models.Model):
    class Meta:
        db_table = "users"

    user_id = models.BigAutoField(primary_key=True)
    user_password = models.TextField(null=False)
    user_firstname = models.CharField(max_length=50)
    user_lastname = models.CharField(max_length=50)
    user_email = models.CharField(max_length=225)
    # user_level = models.CharField
    registration_time = models.BigIntegerField()
    user_DOB = models.DateField()
    user_gender = models.CharField(max_length=1, choices=(('M', 'M'), ('F', 'F')))


class Portals(models.Model):
    class Meta:
        db_table = "portals"

    portal_id = models.BigAutoField(primary_key=True)
    portal_name = models.CharField(max_length=255, null=False)
    portal_desc = models.TextField(null=False)
    time_log = models.BigIntegerField(default=0)
    portal_profile_pic_url = models.TextField(null=False)


class Portals_Users(models.Model):
    class Meta:
        db_table = "portals_users"

    portal_user_id = models.BigAutoField(primary_key=True)
    portal_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    portal_relation_type = models.SmallIntegerField(default=0)


class Posts(models.Model):
    class Meta:
        db_table = "posts"

    post_id = models.BigAutoField(primary_key=True)
    post_name = models.CharField(max_length=255)
    post_desc = models.CharField(max_length=255)
    post_article = models.TextField()
    post_author_portal_id = models.BigIntegerField()
    post_datetime = models.BigIntegerField(default=0)
    post_total_likes = models.IntegerField(default=0)
    post_likes = models.IntegerField(default=0)
    post_dislikes = models.IntegerField(default=0)
    num_root_comments = models.IntegerField(default=0)
    post_type = models.SmallIntegerField()
    num_views = models.BigIntegerField(default=0)


class Posts_Likes_Dislikes(models.Model):
    class Meta:
        db_table = "posts_likes_dislikes"

    likes_dislikes_id = models.BigAutoField(primary_key=True)
    post_id = models.BigIntegerField()
    portal_id = models.BigIntegerField()
    like_or_dislike = models.CharField(max_length=1, choices=(('1', '1'), ('0', '0'), ('-1', '-1')))
    time_log = models.BigIntegerField(default=0)


class Tags(models.Model):
    class Meta:
        db_table = "tags"

    tag_id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(max_length=255)
    tag_desc = models.TextField()
    time_log = models.BigIntegerField()


class Posts_Tags(models.Model):
    class Meta:
        db_table = "posts_tags"

    posts_tags_id = models.BigAutoField(primary_key=True)
    post_id = models.BigIntegerField()
    tag_id = models.BigIntegerField()
    time_log = models.BigIntegerField()


class Portals_Tags(models.Model):
    class Meta:
        db_table = "portals_tags"

    portals_tags_id = models.BigAutoField(primary_key=True)
    tag_id = models.BigIntegerField()
    portal_id = models.BigIntegerField()
    time_log = models.BigIntegerField()


class Portal_Sub_Portal(models.Model):
    class Meta:
        db_table = "portal_sub_portal"

    portal_sub_portal_id = models.BigAutoField(primary_key=True)
    cur_portal_id = models.BigIntegerField(0)
    subed_to_portal_id = models.BigIntegerField()
    time_log = models.BigIntegerField()


class Comments(models.Model):
    class Meta:
        db_table = "comments"

    comment_id = models.BigAutoField(primary_key=True)
    post_id = models.BigIntegerField()
    comment_portal_id = models.BigIntegerField()
    comment_body = models.TextField()
    comment_likes = models.IntegerField(default=0)
    comment_dislikes = models.IntegerField(default=0)
    comment_parent_id = models.BigIntegerField()
    comment_datetime = models.BigIntegerField()
    comment_total_likes = models.IntegerField(default=0)
    comment_level = models.IntegerField(default=0)
    num_child_comments = models.IntegerField(default=0)
    comment_score = models.IntegerField(default=0)
    average_time_per_action = models.FloatField(default=0)
    time_of_last_action = models.BigIntegerField(default=0)


class Comments_Likes_Dislikes(models.Model):
    class Meta:
        db_table = "comments_likes_dislikes"

    likes_dislikes_id = models.BigAutoField(primary_key=True)
    comment_id = models.BigIntegerField()
    portal_id = models.BigIntegerField()
    time_log = models.BigIntegerField()
    like_or_dislike = models.CharField(max_length=1, choices=(('1', '1'), ('0', '0'), ('-1', '-1')))


class Posts_Portals_Rel(models.Model):
    class Meta:
        db_table = "posts_portals_rel"

    posts_portals_rel_id = models.BigAutoField(primary_key=True)
    post_id = models.BigIntegerField()
    portal_id = models.BigIntegerField()
    time_log = models.BigIntegerField()
