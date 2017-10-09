from django.http import HttpRequest
from django.http import HttpResponse

from ..rostrus import Ros_CONST
from .article import Article


def write_post_type_article(request: HttpRequest):
    return HttpResponse(Article.insert_article(request.POST[Ros_CONST.Posts.ARTICLE_TITLE],
                                               request.POST[Ros_CONST.Posts.ARTICLE_DESCRIPTION],
                                               request._PORTAL_ID, request.POST[Ros_CONST.Tags.LIST],
                                               request.POST[Ros_CONST.Posts.ARTICLE_URL]))


def get_for_you_posts(request: HttpRequest):
    return HttpResponse(Article.get_personalized_posts(request._PORTAL_ID))


def get_single_post(request: HttpRequest):
    return HttpResponse(Article.get_single_post(request._PORTAL_ID, request.POST[Ros_CONST.Posts.ID]))


def get_posts_sub_tags(request: HttpRequest):
    return HttpResponse(Article.get_posts_sub_tag(request._PORTAL_ID, request.POST[Ros_CONST.Tags.ID]))


def get_posts_sub_portals(request: HttpRequest):
    return HttpResponse(Article.get_posts_sub_portal(request._PORTAL_ID, request.POST[Ros_CONST.Portal.SUB_ID]))


def update_article(request: HttpRequest):
    return HttpResponse(Article.update_post_article(request._PORTAL_ID, request.POST[Ros_CONST.Posts.ID],
                                                    request.POST[Ros_CONST.Posts.ARTICLE_URL]))


