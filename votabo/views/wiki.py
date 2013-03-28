from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from ..models import (
    DBSession,
    User,
    WikiPage,
    )

import logging

logger = logging.getLogger(__name__)


class WikiPageSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    title = validators.String()
    body = validators.String()


def _get_page(title, rev=None):
    q = DBSession.query(WikiPage).order_by(desc(WikiPage.revision))
    q = q.filter(WikiPage.title == title)
    if rev:
        q = q.filter(WikiPage.revision == int(rev))
    return q.first()


@view_config(request_method="GET", route_name='wiki', renderer='wiki/read.mako', permission="wiki-read")
def wiki_read(request):
    title = request.matchdict["title"]
    index = _get_page(u"wiki:sidebar")
    page = _get_page(title, request.GET.get("revision"))
    if not page:
        return HTTPFound(request.route_url("wiki-edit", title=title))
    return {"index": index, "page": page}


@view_config(request_method="GET", route_name='wiki-edit', renderer='wiki/edit.mako', permission="wiki-update")
@view_config(request_method="PUT", route_name='wiki', renderer='wiki/edit.mako', permission="wiki-update")
def wiki_update(request):
    title = request.matchdict["title"]
    # request.POST["title"] = title
    page = _get_page(title)
    if not page:
        page = WikiPage()
        page.title = title
    form = Form(request, method="PUT", schema=WikiPageSchema, obj=page)

    if form.validate():
        form.bind(page, include=["body", "title"])
        page.revision = (page.revision or 0) + 1  # sqlalchemy "default" doesn't work here?
        page.user = request.user
        page.user_ip = request.user.ip
        DBSession.add(page)
        return HTTPFound(request.route_url("wiki", title=page.title))
    else:
        logger.warning("Form failed validation: %r %r" % (request.POST, form.errors))
        index = _get_page(u"wiki:sidebar")
        return {"form": FormRenderer(form), "page": page, "index": index}


@view_config(request_method="DELETE", route_name='wiki', permission="wiki-delete")
def wiki_delete(request):
    title = request.matchdict["title"]
    page = _get_page(title)
    if page:
        DBSession.delete(page)
        request.session.flash("Deleted page '%s' version %d" % (page.title, page.revision))
    return HTTPFound(request.route_url("wiki", title="index"))
