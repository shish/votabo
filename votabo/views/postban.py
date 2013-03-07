from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import aliased

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    PostBan,
    User,
    )
from ..lib import cache


@view_config(request_method="GET", route_name='postbans', renderer='postban/list.mako', permission="postban-list")
def postban_list(request):
    postbans_per_page = int(request.registry.settings.get("votabo.postbans_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.url, {'page': page})

    sql = DBSession.query(PostBan).order_by(desc(PostBan.id))
    if request.GET.get("fingerprint"):
        sql = sql.filter(PostBan.fingerprint.ilike(request.GET["fingerprint"]))
    if request.GET.get("reason"):
        sql = sql.filter(PostBan.reason.ilike("%"+request.GET["reason"]+"%"))
    postbans = Page(sql, page=page, items_per_page=postbans_per_page, url=url_for_page)
    return {"postbans": postbans, "pager": postbans}
