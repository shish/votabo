from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import NotFound
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

import logging
logger = logging.getLogger(__name__)


class UserSettingsException(Exception):
    pass


class PasswordChangeException(UserSettingsException):
    pass


def good_password(pw):
    return len(pw) > 5


@view_config(request_method="GET", route_name='user', renderer='user/read.mako')
def user_read(request):
    name = request.matchdict["name"]
    duser = DBSession.query(User).filter(User.username == name).first()
    if not duser:
        raise NotFound("User '%s' not found" % name)
    return {"duser": duser}


#@view_config(request_method="PUT", route_name='user', permission="edit-user-self", match_param={"name": "_self"})
@view_config(request_method="PUT", route_name='user', permission="edit-user")
def user_update(request):
    name = request.matchdict["name"]
    if name == "_self":
        duser = request.user
    else:
        duser = DBSession.query(User).filter(User.username == name).first()

    logger.info("Trying to update info for User %s (%s)" % (duser.username, name))

    if name == "_self" and not duser.check_password(request.POST.get("current_password", "")):
        raise UserSettingsException("Current password not entered")

    if request.POST.get("new_password_1"):
        if not good_password(request.POST.get("new_password_1")):
            raise PasswordChangeException("Too weak")
        if request.POST.get("new_password_1") != request.POST.get("new_password_2"):
            raise PasswordChangeException("Passwords don't match")
        logger.info("Updating password for User %s" % (duser.username))
        duser.set_password(request.POST["new_password_1"])

    if "email" in request.POST and request.POST["email"] != duser.email:
        new = request.POST["email"] or None
        logger.info("Updating email for User %s (%r -> %r)" % (duser.username, duser.email, new))
        duser.email = new

    return HTTPFound(request.referrer or request.route_url('user', name=duser.username))


@view_config(request_method="GET", route_name='users', renderer='user/list.mako', permission="user-list")
def user_list(request):
    users_per_page = int(request.registry.settings.get("votabo.users_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.path, request.params)

    sql = DBSession.query(User).order_by(desc(User.id))
    if request.GET.get("id"):
        sql = sql.filter(User.id == request.GET["id"])
    if request.GET.get("username"):
        sql = sql.filter(User.username.ilike("%" + request.GET["username"] + "%"))
    if request.GET.get("email"):   # FIXME: has_permission(edit-user) -- else info could leak by blind searching
        sql = sql.filter(User.email.ilike("%" + request.GET["email"] + "%"))
    if request.GET.get("posts"):
        sql = sql.filter(User.post_count >= int(request.GET["posts"].replace("on", "1")))
    if request.GET.get("comments"):
        sql = sql.filter(User.comment_count >= int(request.GET["comments"].replace("on", "1")))
    if request.GET.get("category"):
        sql = sql.filter(User.category == request.GET["category"])
    users = Page(sql, page=page, items_per_page=users_per_page, url=url_for_page)
    return {"users": users, "pager": users}
