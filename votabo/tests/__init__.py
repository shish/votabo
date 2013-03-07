import unittest2
import transaction

from pyramid import testing

from votabo import *

from votabo.lib import cache
from votabo.models import (
    DBSession,
    Base,
    User,
    Post,
    Tag
    )


class VotaboTest(unittest2.TestCase):
    def setUp(self):
        self.config = testing.setUp()

        configure_routes(self.config)
        configure_templates(self.config)
        configure_locale(self.config)
        configure_user(self.config)
        #configure_auth(self.config)

        cache.fast.configure("dogpile.cache.memory")
        cache.slow.configure("dogpile.cache.memory")

        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            u = User()
            u.username = u"test-admin"
            u.category = "admin"
            u.email = "test@example.com"
            u.password = "0"*32

            p = Post()
            p.fingerprint = "0"*32
            p.tags.append(Tag(u"test-tag"))

            u.posts.append(p)

            DBSession.add(u)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

        cache.slow = cache.make_region()
        cache.fast = cache.make_region()
