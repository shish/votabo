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


@view_config(request_method="GET", route_name='tags', renderer='json', request_param="format=json")
@view_config(request_method="GET", route_name='tags', renderer='json', xhr=True)
@view_config(request_method="GET", route_name='tags', renderer='tag/list.mako')
def tag_list(request):
    tags = DBSession.query(Tag).order_by(Tag.name)

    starts_with = request.GET.get("starts_with", u"a")

    if starts_with == "?":  # pragma: no cover -- postgres only
        f = Tag.name.op("~")("^[^a-zA-Z]")
    else:
        f = Tag.name.ilike(starts_with + "%")
    tags = tags.filter(f)

    tags_min = int(request.GET.get("tags_min", request.registry.settings.get("votabo.default_tags_min", "1")))
    tags = tags.filter(Tag.count >= tags_min)

    return {"tags": tags, "starts_with": starts_with, "tags_min": tags_min}

