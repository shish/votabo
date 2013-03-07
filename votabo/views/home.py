from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    User,
    Post,
    Tag,
    Comment,
    )


@view_config(route_name='home', renderer='home.mako')
def home(request):
    post_count = DBSession.query(Post).count()
    return {"site_title": request.registry.settings.get("votabo.site_title"), "post_count": post_count}
