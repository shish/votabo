from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

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

import logging

logger = logging.getLogger(__name__)


class IPBanExistsException(Exception):
    pass


@view_config(request_method="POST", route_name='ipbans', permission="ipban-create")
def ipban_create(request):
    existing = DBSession.query(IPBan).filter(IPBan.ip.ilike(request.POST["ip"])).first()
    if existing:
        raise IPBanExistsException("%s is already banned (until %s for %s)" % (existing.ip, existing.until, existing.reason))

    end = request.POST["until"].strip()
    ipban = IPBan(banner=request.user, ip=request.POST["ip"].strip(),
        reason=request.POST["reason"].strip(), until=end)
    logger.info("Create ipban for %s because %s", ipban.ip, ipban.reason)
    DBSession.add(ipban)
    DBSession.flush()
    return HTTPFound(request.route_url('ipbans'), headers=[("X-VTB-Ban-ID", ipban.id)])


@view_config(request_method="GET", route_name='ipbans', renderer='ipban/list.mako', permission="ipban-list")
def ipban_list(request):
    ipbans_per_page = int(request.registry.settings.get("votabo.ipbans_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.path, request.params)

    sql = DBSession.query(IPBan).order_by(desc(IPBan.id))
    if request.GET.get("ip"):
        if "/" not in request.GET["ip"]:
            sql = sql.filter(IPBan.ip == request.GET["ip"])
        else:  # pragma: no cover -- requires postgres
            sql = sql.filter(IPBan.ip.op(">>=")(request.GET["ip"]))
    if request.GET.get("reason"):
        sql = sql.filter(IPBan.reason.ilike("%" + request.GET["reason"] + "%"))
    if request.GET.get("banner"):
        sql = sql.join(User).filter(User.username.ilike(request.GET["banner"]))
    ipbans = Page(sql, page=page, items_per_page=ipbans_per_page, url=url_for_page)
    return {"ipbans": ipbans, "pager": ipbans}


@view_config(request_method="DELETE", route_name='ipban', permission="ipban-delete")
def ipban_delete(request):
    bid = request.matchdict["id"]
    ipban = DBSession.query(IPBan).filter(IPBan.id == bid).first()
    if ipban:
        logger.info("Deleting ban for %s", ipban.ip)
        DBSession.delete(ipban)
    return HTTPFound(request.referrer or request.route_url('ipbans'))
