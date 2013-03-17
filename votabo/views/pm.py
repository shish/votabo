from pyramid.view import view_config
from pyramid.exceptions import Forbidden

from sqlalchemy import desc

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    PrivateMessage,
    )


@view_config(request_method="GET", route_name='pms', renderer='pm/list.mako', permission="pm-list")
def pm_list(request):
    pms_per_page = int(request.registry.settings.get("votabo.pms_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.url, {'page': page})

    sql = DBSession.query(PrivateMessage).order_by(desc(PrivateMessage.id))
    pms = Page(sql, page=page, items_per_page=pms_per_page, url=url_for_page)
    return {"pms": pms, "pager": pms}


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
