from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    Alias,
    Post,
    Tag,
    Alias,
    Comment,
    )

import logging

logger = logging.getLogger(__name__)

class AliasExistsException(Exception):
    pass


class AliasLoopException(Exception):
    pass


@view_config(request_method="POST", route_name='aliases', permission="alias-create")
def alias_create(request):
    existing = DBSession.query(Alias).filter(Alias.oldtag.ilike(request.POST["oldtag"])).first()
    if existing:
        raise AliasExistsException("%s is already an alias (for %s)" % (existing.oldtag, existing.newtag))

    is_alias = DBSession.query(Alias).filter(Alias.oldtag.ilike(request.POST["newtag"])).first()
    if is_alias:
        raise AliasLoopException("%s is already an alias (for %s), can't create an alias to an alias" % (is_alias.oldtag, is_alias.newtag))

    alias = Alias(request.POST["oldtag"].strip(), request.POST["newtag"].strip())
    logger.info("Create alias from %s to %s", alias.oldtag, alias.newtag)
    DBSession.add(alias)
    return HTTPFound(request.route_url('aliases'))


@view_config(request_method="GET", route_name='aliases', renderer='alias/list.mako', permission="alias-list")
def alias_list(request):
    aliases_per_page = int(request.registry.settings.get("votabo.aliases_per_page", 50))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.url, {'page': page})

    sql = DBSession.query(Alias).order_by(Alias.newtag)
    if request.GET.get("oldtag"):
        sql = sql.filter(Alias.oldtag.ilike("%"+request.GET["oldtag"]+"%"))
    if request.GET.get("newtag"):
        sql = sql.filter(Alias.newtag.ilike("%"+request.GET["newtag"]+"%"))
    aliases = Page(sql, page=page, items_per_page=aliases_per_page, url=url_for_page)
    return {"aliases": aliases, "pager": aliases}


@view_config(request_method="DELETE", route_name='alias', permission="alias-delete")
def alias_delete(request):
    aid = request.matchdict["id"]
    alias = DBSession.query(Alias).filter(Alias.oldtag==aid).first()
    if alias:
        logger.info("Deleting alias from %s to %s", alias.oldtag, alias.newtag)
        DBSession.delete(alias)
    return HTTPFound(request.route_url('aliases'))  # FIXME: referrer
