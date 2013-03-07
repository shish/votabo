from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import aliased

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    IPBan,
    User,
    )
from ..lib import cache


@view_config(request_method="GET", route_name='ipbans', renderer='ipban/list.mako', permission="ipban-list")
def ipban_list(request):
    ipbans_per_page = int(request.registry.settings.get("votabo.ipbans_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.url, {'page': page})

    sql = DBSession.query(IPBan).order_by(desc(IPBan.id))
    if request.GET.get("ip"):
        sql = sql.filter(IPBan.ip.op(">>=")(request.GET["ip"]))
    if request.GET.get("reason"):
        sql = sql.filter(IPBan.reason.ilike("%"+request.GET["reason"]+"%"))
    if request.GET.get("banner"):
        sql = sql.join(User).filter(User.username.ilike(request.GET["banner"]))
    ipbans = Page(sql, page=page, items_per_page=ipbans_per_page, url=url_for_page)
    return {"ipbans": ipbans, "pager": ipbans}
