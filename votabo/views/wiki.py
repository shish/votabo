from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    User,
    WikiPage,
    )


@view_config(request_method="GET", route_name='wiki', renderer='wiki/read.mako')
def wiki_read(request):
    title = request.matchdict["title"]
    index = DBSession.query(WikiPage).filter(WikiPage.title == u"wiki:sidebar").order_by(desc(WikiPage.revision)).first()
    page = DBSession.query(WikiPage).filter(WikiPage.title == title).order_by(desc(WikiPage.revision)).first()
    if not page:
        page = WikiPage()
    return {"index": index, "page": page}
