from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import aliased

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    LogEvent,
    )
from ..lib import cache


@cache.fast.cache_on_arguments(expiration_time=600)
def _count_events():
    return DBSession.query(LogEvent).count()


@view_config(request_method="GET", route_name='logs', renderer='log/list.mako', permission="log-list")
def log_list(request):
    logs_per_page = int(request.registry.settings.get("votabo.logs_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.path, request.params)

    sql = DBSession.query(LogEvent).order_by(desc(LogEvent.id))
    if request.GET.get("module"):
        sql = sql.filter(LogEvent.section.ilike(request.GET["module"]))
    if request.GET.get("username"):
        sql = sql.filter(LogEvent.username.ilike(request.GET["username"]))
    if request.GET.get("message"):
        sql = sql.filter(LogEvent.message.ilike(request.GET["message"] + "%"))
    if request.GET.get("address"):
        sql = sql.filter(LogEvent.address.op("<<=")(request.GET["address"]))
    logs = Page(sql, page=page, items_per_page=logs_per_page, url=url_for_page, item_count=_count_events())
    return {"logs": logs, "pager": logs}
