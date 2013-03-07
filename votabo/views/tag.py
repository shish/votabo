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
def tag_list_xhr(request):
    starts_with = request.GET.get("starts_with", u"a")
    tags_min = 12
    if starts_with == "?":
        f = Tag.name.op("~")("^[^a-zA-Z]")
    else:
        f = Tag.name.ilike(starts_with+"%")
    tags = DBSession.query(Tag).filter(f).filter(Tag.count > tags_min).order_by(Tag.name)
    tags = [{"name": tag.name, "count": tag.count} for tag in tags]
    return {"tags": tags, "starts_with": starts_with, "tags_min": tags_min}


@view_config(request_method="GET", route_name='tags', renderer='tag/list.mako')
def tag_list(request):
    starts_with = request.GET.get("starts_with", u"a")
    tags_min = 12
    if starts_with == "?":
        f = Tag.name.op("~")("^[^a-zA-Z]")
    else:
        f = Tag.name.ilike(starts_with+"%")
    tags = DBSession.query(Tag).filter(f).filter(Tag.count > tags_min).order_by(Tag.name)
    return {"tags": tags, "starts_with": starts_with, "tags_min": tags_min}

