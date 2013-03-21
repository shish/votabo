from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    User,
    Post,
    Tag,
    Comment,
    )
from ..lib import cache
import logging

logger = logging.getLogger(__name__)


@cache.fast.cache_on_arguments(expiration_time=600)
def _count_comments():
    return DBSession.query(Comment).count()


@view_config(request_method="GET", route_name='comments', renderer='comment/list.mako')
def comment_list(request):
    page = int(request.GET.get("page", "1"))
    comments_per_page = int(request.registry.settings.get("votabo.comments_per_page", 20))
    url_for_page = PageURL(request.route_path('comments'), {'page': page})
    sql = DBSession.query(Comment).order_by(desc(Comment.id))
    comments = Page(sql, page=page, items_per_page=comments_per_page, url=url_for_page, item_count=_count_comments())
    return {"comments": comments, "pager": comments}


@view_config(request_method="POST", route_name='comments', permission='comment-create')
def comment_create(request):
    post_id = int(request.POST["post"])
    comment = request.POST["comment"]

    post = DBSession.query(Post).get(post_id)
    post.comments.append(Comment(request.user, request.remote_addr, comment))
    return HTTPFound(request.route_url("post", id=post_id))


@view_config(request_method="DELETE", route_name='comment', permission='comment-delete')
def comment_delete(request):
    cid = request.matchdict["id"]
    comment = DBSession.query(Comment).filter(Comment.id == cid).first()
    if comment:
        logger.info("Deleting comment %d", comment.id)
        DBSession.delete(comment)
    return HTTPFound(request.route_url('comments'))  # FIXME: referrer
