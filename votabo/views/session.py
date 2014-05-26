from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from ..models import (
    DBSession,
    User,
    )


class VotoboException(Exception):
    pass


class SessionException(VotoboException):
    pass


@view_config(request_method="POST", route_name='session')
def session_create(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    duser = User.by_name(username)
    if duser and duser.check_password(password):
        request.response.headers.extend(remember(request, duser))
        return HTTPFound(request.route_url('user', name=duser.username), headers=request.response.headers)
    else:
        raise SessionException("No user with those details was found")


@view_config(request_method="GET", route_name='session-delete')  # FIXME: get = bad
def session_delete(request):
    request.response.headers.extend(forget(request))
    return HTTPFound(request.route_url('posts'), headers=request.response.headers)
