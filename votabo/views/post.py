from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc, func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import aliased

from webhelpers.paginate import PageURL, Page

from ..models import (
    DBSession,
    User,
    Post,
    Tag,
    Comment,
    map_post_tag,
    )
from ..lib import cache

import logging
from base64 import b64decode

logger = logging.getLogger(__name__)


@cache.fast.cache_on_arguments(expiration_time=600)
def _count_posts():
    return DBSession.query(Post).count()


class PostSearch(object):
    def __init__(self, query):
        self.query = Tag.split(query)

#    def _get_ids__tag(self, tag):
#        ids = []
#        for row in DBSession.query(map_post_tag).join(Tag).filter(Tag.name == tag).all():
#            ids.append(row.image_id)
#        return ids

    def filter(self, sql):
        plain = []
        for item in self.query:
            t = Tag.get(item)
            if not t:
                logger.info("Couldn't find tag for '%s' - shortcutting", item)
                sql = sql.filter("1=0")
            elif t.is_plain_tag():
                plain.append(t.name)
        if plain:
            sql = sql.join(Post.tags).filter(Tag.name.in_(plain)).group_by(Post.id).having(func.count(Post.id) == len(plain))
        return sql


@view_config(request_method="GET", route_name='posts', renderer='post/list.mako')
def post_list(request):
    query = PostSearch(request.GET.get("q", ""))
    posts_per_page = int(request.registry.settings.get("votabo.posts_per_page", 24))
    page = int(request.GET.get("page", "1"))
    url_for_page = PageURL(request.url, {'page': page})

    sql = DBSession.query(Post).order_by(desc(Post.id))
    sql = query.filter(sql)
    posts = Page(sql, page=page, items_per_page=posts_per_page, url=url_for_page, item_count=_count_posts())
    return {"query": request.GET.get("q"), "posts": posts, "pager": posts}


@view_config(request_method="GET", route_name='posts/upload', renderer='post/upload.mako')
def post_upload(request):
    return {}


@view_config(request_method="POST", route_name='posts', renderer="json", xhr=True)
def post_create_xhr(request):
    logger.info("Uploading %s with XHR", request.POST.get("filename"))
    try:
        p = Post()
        p.filename = request.POST.get("filename")
        p.mimetype = request.POST.get("mimetype")
        p.data = request.POST.get("data")
        # DBSession.add(p)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@view_config(request_method="POST", route_name='posts')
def post_create(request):
    tags = Tag.split(request.POST.get("tags"))

    for fobj in request.POST.getall("file"):
        if fobj != "":
            logger.info("Uploading file: %s with tags %s", fobj, tags)
            p = Post()
            p.filename = fobj.filename
            p.mimetype = fobj.type
            p.data = fobj.file.read()
            # DBSession.add(p)

    for fdat in request.POST.getall("data"):
        if fdat != "":
            logger.info("Uploading data: %s with tags %s", fdat, tags)

    return HTTPFound(request.route_url('posts'))


@view_config(request_method="GET", route_name='post', renderer='post/read.mako')
def post_read(request):
    pid = request.matchdict["id"]
    post = DBSession.query(Post).filter(Post.id == pid).one()
    return {"post": post}
