import unittest2
import transaction

from pyramid import testing
from hashlib import md5
import json

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
        # configure_auth(self.config)

        cache.fast.configure("dogpile.cache.memory")
        cache.slow.configure("dogpile.cache.memory")

        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            u1 = User()
            u1.username = u"test-admin"
            u1.category = "admin"
            u1.email = "test-admin@example.com"
            u1.password = md5(u1.username + "password").hexdigest()

            p1 = Post()
            p1.fingerprint = "0"*32
            p1.tags.append(Tag(u"test-tag"))

            u1.posts.append(p1)

            DBSession.add(u1)

            u2 = User()
            u2.username = u"test-user"
            u2.category = "user"
            u2.email = "test-user@example.com"
            u2.password = md5(u2.username + "password").hexdigest()
            DBSession.add(u2)

            u3 = User()
            u3.username = u"test-user2"
            u3.category = "user"
            u3.email = "test-user2@example.com"
            u3.password = md5(u3.username + "password").hexdigest()
            DBSession.add(u3)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

        cache.slow = cache.make_region()
        cache.fast = cache.make_region()
