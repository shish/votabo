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


class WikiPageSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    title = validators.String()
    body = validators.String()


@view_config(request_method="GET", route_name='wiki', renderer='wiki/read.mako', permission="wiki-read")
def wiki_read(request):
    title = request.matchdict["title"]
    index = DBSession.query(WikiPage).filter(WikiPage.title == u"wiki:sidebar").order_by(desc(WikiPage.revision)).first()
    page = DBSession.query(WikiPage).filter(WikiPage.title == title).order_by(desc(WikiPage.revision)).first()
    if not page:
        return HTTPFound(request.route_url("wiki-edit", title=title))
    return {"index": index, "page": page}


@view_config(request_method="GET", route_name='wiki-edit', renderer='wiki/edit.mako', permission="wiki-update")
@view_config(request_method="PUT", route_name='wiki', permission="wiki-update")
def wiki_update(request):
    title = request.matchdict["title"]
    page = DBSession.query(WikiPage).filter(WikiPage.title == title).order_by(desc(WikiPage.revision)).first()
    if not page:
        page = WikiPage()
        page.title = title
    form = Form(request, schema=WikiPageSchema, obj=page)

    if form.validate():
        form.bind(page, include=["body", "title"])
        page.revision = (page.revision or 0) + 1  # sqlalchemy doesn't work here?
        page.user = request.user
        page.user_ip = request.user.ip
        DBSession.add(page)
        return HTTPFound(request.route_url("wiki", title=page.title))
    else:
        return {"form": FormRenderer(form)}


@view_config(request_method="DELETE", route_name='wiki', permission="wiki-delete")
def wiki_delete(request):
    title = request.matchdict["title"]
    page = DBSession.query(WikiPage).filter(WikiPage.title == title).order_by(desc(WikiPage.revision)).first()
    if page:
        DBSession.delete(page)
        request.session.flash("Deleted page '%s' version %d" % (page.title, page.revision))
    return HTTPFound(request.route_url("wiki", title="index"))
