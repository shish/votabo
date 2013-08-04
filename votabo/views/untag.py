from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import aliased

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    UnTag,
    User,
    )
from ..lib import cache

import logging

logger = logging.getLogger(__name__)


class UnTagExistsException(Exception):
    pass


@view_config(request_method="POST", route_name='untags', permission="untag-create")
def untag_create(request):
    existing = DBSession.query(UnTag).filter(UnTag.tag.ilike(request.POST["tag"])).first()
    if existing:
        raise UnTagExistsException("%s is already a redirect to %s" % (existing.tag, existing.redirect))

    untag = UnTag(tag=request.POST["tag"].strip(), redirect=request.POST["redirect"].strip())
    logger.info("Create untag for %s because %s", untag.tag, untag.redirect)
    DBSession.add(untag)
    DBSession.flush()
    return HTTPFound(request.route_url('untags'))


@view_config(request_method="GET", route_name='untags', renderer='untag/list.mako', permission="untag-list")
def untag_list(request):
    untags_per_page = int(request.registry.settings.get("votabo.untags_per_page", 200))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.path, request.params)

    sql = DBSession.query(UnTag).order_by(desc(UnTag.tag))
    if request.GET.get("tag"):
        sql = sql.filter(UnTag.tag.ilike("%" + request.GET["tag"] + "%"))
    if request.GET.get("redirect"):
        sql = sql.filter(UnTag.redirect.ilike("%" + request.GET["redirect"] + "%"))
    untags = Page(sql, page=page, items_per_page=untags_per_page, url=url_for_page)
    return {"untags": untags, "pager": untags}


@view_config(request_method="DELETE", route_name='untag', permission="untag-delete")
def untag_delete(request):
    tag = request.matchdict["tag"]
    untag = DBSession.query(UnTag).filter(UnTag.tag == tag).first()
    if untag:
        logger.info("Deleting untag for %s", untag.tag)
        DBSession.delete(untag)
    return HTTPFound(request.referrer or request.route_url('untags'))
