import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession, Base,
    User, PrivateMessage, IPBan,
    WikiPage,
    Post, Tag, Comment
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        anon = User(username="Anonymous", password="[blocked]", category="anonymous")
        system = User(username="System", password="[blocked]", category="anonymous")
        admin = User(username="Admin", password="", category="admin")
        DBSession.add_all([anon, system, admin])

        pm = PrivateMessage(user_from=system, user_to=admin, subject="Welcome to Votabo", message="Hello!")
        DBSession.add(pm)

        ipban = IPBan(banner=system, ip="127.0.0.2", reason="test", end_timestamp=0)
        DBSession.add(ipban)

        wp = WikiPage(user=anon, user_ip="127.0.0.1", title=":default:", body="this is a default wiki page")
        DBSession.add(wp)

        post = Post(user=system, fingerprint="", width=100, height=100)
        post.tags.append(Tag("cat"))
        post.tags.append(Tag("cute"))
        post.comments.append(Comment(user=system, user_ip="127.0.0.1", body="cute!"))
        DBSession.add(post)
