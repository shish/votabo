from pyramid.view import view_config
from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    PrivateMessage,
    User,
    )

import logging

logger = logging.getLogger(__name__)


@view_config(request_method="GET", route_name='pms', renderer='pm/list.mako', permission="pm-list")
def pm_list(request):
    pms_per_page = int(request.registry.settings.get("votabo.pms_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.path, request.params)

    sql = DBSession.query(PrivateMessage).order_by(desc(PrivateMessage.id))
    pms = Page(sql, page=page, items_per_page=pms_per_page, url=url_for_page)
    return {"pms": pms, "pager": pms}


@view_config(request_method="POST", route_name='pms', permission="pm-create")
def pm_create(request):
    user_to = User.by_name(request.POST["to"])
    if not user_to:
        raise Exception("Target user '%s' not found" % (request.POST["to"]))
    # TODO: don't allow sending PMs to anonymous etc
    #if not user_to.has_permission('read-pm'):
    #    raise Exception("Target user can't read PMs")

    pm = PrivateMessage(user_from=request.user, user_to=user_to, subject=request.POST["subject"], message=request.POST["message"])
    logger.info("Create pm '%s' from %s to %s", pm.subject, pm.user_from.username, pm.user_to.username)
    DBSession.add(pm)
    
    return HTTPFound(request.referrer or request.route_url('pms'))


@view_config(request_method="GET", route_name='pm', renderer='pm/read.mako', permission="pm-read")
def pm_read(request):
    pid = request.matchdict["id"]
    pm = DBSession.query(PrivateMessage).filter(PrivateMessage.id == pid).first()
    if pm.user_to == request.user:
        pm.is_read = True
        return {"pm": pm}
    elif request.user.category == "admin":  # FIXME has_permission
        return {"pm": pm}
    else:
        raise Forbidden("That's not your PM")
    

@view_config(request_method="DELETE", route_name='pm', permission="pm-delete")
def pm_delete(request):
    pid = request.matchdict["id"]
    pm = DBSession.query(PrivateMessage).filter(PrivateMessage.id == pid).first()
    if pm.user_to == request.user or request.user.category == "admin":
        DBSession.delete(pm)
    else:
        raise Forbidden("That's not your PM")
    
    return HTTPFound(request.referrer or request.route_url('pms'))
