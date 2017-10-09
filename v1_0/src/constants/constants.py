class _COMMENTS_Const:
    DATA_NAME = "comments"
    ID = "comm_id"
    PORTAL_ID = "comm_portal_id"
    PORTAL_NAME = "comm_portal_name"
    TEXT_BODY = "comm_body"
    DISLIKES = "comm_dislikes"
    LIKES = "comm_likes"
    LIKE_OR_DISLIKE = "comm_like_or_dislike"
    PARENT_ID = "comm_parent_id"
    PUB_TIME = "comm_datetime"
    POST_ID = "comm_post_id"
    LEVEL = "comm_level"
    OFFSET = "comm_offset"
    NUM_NEEDED = "comm_num_req"
    NUM_REPLIES = "comm_num_replies"
    PORTAL_PIC_URL = "comm_portal_pic_url"
    SCORE = "comment_score"
    REPLIES = "comm_replies"
    NUM_ROOT_COMMENTS = "comm_num_root_comments"
    REPLIES_AVAIL = "comm_available_bool"


class _LOGIN_REGISTRATION_Const:
    LOGIN_TYPE = "login_type"
    LOGIN_FAIL = -1
    JWT_TOKEN = "user_token"
    LOGIN_TYPE_EMAIL = "1"
    LOGIN_TYPE_FACEBOOK = "2"

    FACEBOOK_ACCESS_ID = "facebook_access_id"

    REGIS_ERROR = "error"
    REGIS_SUCCESS = "ok"

    DEVICE_TYPE = "device_type"
    DEVICE_ID = "device_id"


class _CRED_Const:
    AWS = "aws_cred"
    AWS_region = "aws_region"
    AWS_key = "aws_key"
    AWS_identity_pool_id = "aws_identity_pool_id"
    AWS_secret = "aws_secret"

    JWT = "jwt"
    JWT_secret = "secret"

    REDIS = "redis_db_cred"
    REDIS_host = "redis_host"

    MYSQL = "mysql_db_cred"
    MYSQL_username = "db_username"
    MYSQL_host = "db_host"
    MYSQL_name = "db_name"
    MYSQL_password = "db_password"


class _POSTS_Const:
    NUM_LIKES = "post_likes"
    NUM_DISLIKES = "post_dislikes"
    TOTAL_LIKES = "post_total_likes"
    ID = "post_id"
    LIKED_OR_DISLIKED = "post_like_or_dislike"
    NUM_ROOT_COMMENTS = "post_num_comments"
    NUM_VIEWS = "post_num_views"
    DATETIME = "post_datetime"
    SCORE = "post_score"
    LIKE = "1"
    DISLIKE = "-1"
    NOT_LIKE_DISLIKE = "0"

    TYPE = "post_type"
    TYPE_ARTICLE = "0"
    TYPE_UPDATE = "1"

    ARTICLE_URL = "post_article_content"
    ARTICLE_TITLE = "post_article_title"
    ARTICLE_DESCRIPTION = "post_article_desc"

    UPDATE_URL_LIST = "post_update_image_url"
    UPDATE_TEXT = "post_update_text"
    UPDATE_TITLE = "post_update_title"
    UPDATE_TITLE_PRESENT = "post_update_title_is_present"


class _ERRORS_Const:
    POST_VARIABLE_NS = "error_post_data"
    ERROR = "error"


class _TAGS_Const:
    TAGS = "tags"
    ID = "tag_id"
    NAME = "tag_name"
    DESC = "tag_desc"
    TIME = "tag_time"
    IS_SUBED = "tag_is_subed"
    TAGS_AVAILABLE = "tags_available"
    LIST = "tags_list"


class _PORTAL_Const:
    ID = "portal_id"
    NAME = "portal_name"
    PIC_URL = "portal_profile_pic_url"
    TIME_LOG = "portal_time_log"
    DESCRIPTION = "portal_desc"
    USER_PORTAL_REL = "portal_user_rel"

    SUB_ID = "portal_sub_id"
    SUB_NAME = "portal_sub_name"
    SUB_PIC_URL = "portal_sub_pic_url"
    SUB_DESC = "portal_sub_desc"
    SUB_TIME = "portal_sub_time"
    SUB_IS_SUBED = "portal_sub_is_subed"


class _USERS_Const:
    PASSWORD = "password"
    EMAIL = "user_email"
    FIRST_NAME = "user_fname"
    LAST_NAME = "user_lname"
    USERNAME = "username"
    USER_ID = "user_id"

    LEVEL = "user_level"
    PROFILE_PIC_URL = "user_profile_pic_url"

    GENDER = "user_gender"
    DOB = "user_date_of_birth"
    REGIS_TIME = "user_regis_time"


class Ros_CONST:
    Portal = _PORTAL_Const()
    Comments = _COMMENTS_Const()
    Posts = _POSTS_Const()
    Users = _USERS_Const()
    LOGIN_REGIS = _LOGIN_REGISTRATION_Const()
    Cred = _CRED_Const()
    Tags = _TAGS_Const()
    Error = _ERRORS_Const()
