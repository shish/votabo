from pyramid.response import Response
from pyramid.view import view_config

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


@view_config(request_method="GET", route_name='user', renderer='user/read.mako')
def user_read(request):
    name = request.matchdict["name"]
    duser = DBSession.query(User).filter(User.username == name).first()
    return {"duser": duser}


@view_config(request_method="GET", route_name='users', renderer='user/list.mako', permission="user-list")
def user_list(request):
    users_per_page = int(request.registry.settings.get("votabo.users_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.url, {'page': page})

    sql = DBSession.query(User).order_by(desc(User.id))
    if request.GET.get("id"):
        sql = sql.filter(User.id == request.GET["id"])
    if request.GET.get("username"):
        sql = sql.filter(User.username.ilike("%"+request.GET["username"]+"%"))
    if request.GET.get("posts"):
        sql = sql.filter(User.post_count > 0)
    if request.GET.get("comments"):
        sql = sql.filter(User.comment_count > 0)
    if request.GET.get("category"):
        sql = sql.filter(User.category == request.GET["category"])
    users = Page(sql, page=page, items_per_page=users_per_page, url=url_for_page)
    return {"users": users, "pager": users}
