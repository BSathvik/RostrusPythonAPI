from django.conf.urls import url


from .src import user_portal, posts, comments, subscriptions, reactions
from . import views

from .src.ros_init import Rostrus_Application

Rostrus_Application.initialise_application()

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^test/?$', user_portal.views.test, name='test'),
    url(r'^db_test/?$', user_portal.views.db_test, name='db_test'),


    url(r'^register/?$', user_portal.views.register, name='register'),

    url(r'^rostrus_login/?$', user_portal.views.rostrus_login, name='rostrus_login'),
    url(r'^facebook_login/?$', user_portal.views.facebook_login, name='fb_login'),

    url(r'^get_portal_prof_img_auth/?$', user_portal.views.get_portal_prof_img_upload_auth, name='get_google_cloud_token'),

    url(r'^posts/write_post_type_article?$', posts.views.write_post_type_article, name='insert_article'),
    url(r'^posts/modify_article?$', posts.views.update_article, name='modify_article'),
    url(r'^posts/get_general_post_data?$', posts.views.get_for_you_posts, name='get_general_post_data'),
    url(r'^posts/get_posts_of_tag?$', posts.views.get_posts_sub_tags, name='get_posts_from_sub_tags'),
    url(r'^posts/get_posts_of_portal?$', posts.views.get_posts_sub_portals, name='get_posts_from_sub_portals'),
    url(r'^posts/get_single_post_data?$', posts.views.get_single_post, name='get_single_post'),

    url(r'^comments/write_comment?$', comments.views.write_comment, name='insert_comment'),
    url(r'^comments/get_comments?$', comments.views.get_comments, name='get_comment'),
    url(r'^comments/delete_comment?$', comments.views.delete_comment, name='del_comment'),

    url(r'^profile/upload_profile_pic_url?$', user_portal.views.update_profile_pic_url, name='update_prof_pic'),
    url(r'^profile/delete_profile_pic?$', user_portal.views.del_profile_pic, name='del_profile_pic'),

    url(r'^subscriptions/get_portal_subscriptions?$', subscriptions.views.get_subed_portals, name='get_portal_sub'),
    url(r'^subscriptions/get_tag_subscriptions?$', subscriptions.views.get_portal_sub_tags, name='get_tag_sub'),
    url(r'^subscriptions/subscribe_tag?$', subscriptions.views.sub_tag, name='sub_tag'),
    url(r'^subscriptions/subscribe_portal?$', subscriptions.views.sub_portal, name='sub_portal'),

    url(r'^reactions/update_post_reaction?$', reactions.views.post_reaction_update, name='react_post_update'),
    url(r'^reactions/update_comment_reaction?$', reactions.views.comm_reaction_update, name='react_comm_update'),


]