from pyramid.security import Everyone, Authenticated
from pyramid.security import Allow, Deny
from pyramid.security import ALL_PERMISSIONS

from hashlib import md5

from votabo.models import User


class RootFactory(object):
    __acl__ = [
        (Allow, "u:Shish", ALL_PERMISSIONS),
        (Allow, "g:admin", ALL_PERMISSIONS),

        #(Allow, Authenticated, (
        (Allow, "g:user", (
            'comment-create',
            'pm-list', 'pm-read',
            'alias-list',
        )),
        (Deny, "g:failures", ALL_PERMISSIONS),
        (Allow, "g:something", (
            'something-action',
        )),

        (Deny, Everyone, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        pass


class ShimmieAuthenticationPolicy(object):
    def authenticated_userid(self, request):
        u = User.by_session(
            request,
            request.cookies.get("shm_user"),
            request.cookies.get("shm_session")
        )
        if u:
            return u.username
        else:
            return None

    def unauthenticated_userid(self, request):
        return request.cookies.get("shm_user")

    def effective_principals(self, request):
        if request.user:
            return ["u:"+request.user.username, "g:"+request.user.category]
        else:
            return []

    def remember(self, request, duser, **kw):
        request.response.set_cookie('shm_user', duser.username)
        request.response.set_cookie('shm_session', md5(duser.password + request.remote_addr).hexdigest())

    def forget(self, request):
        request.response.delete_cookie('shm_user')
        request.response.delete_cookie('shm_session')
