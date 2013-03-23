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
    Post, Tag,
    WikiPage,
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
            # admin
            self.user0 = User()
            self.user0.username = u"test-admin"
            self.user0.category = "admin"
            self.user0.email = "test-admin@example.com"
            self.user0.password = md5(self.user0.username + "password").hexdigest()

            p1 = Post()
            p1.fingerprint = "0"*32
            p1.tags.append(Tag.get_or_create(u"test-tag"))
            p1.tags.append(Tag.get_or_create(u"cat"))

            self.user0.posts.append(p1)

            DBSession.add(self.user0)

            # user
            self.user1 = User()
            self.user1.username = u"test-user1"
            self.user1.category = "user"
            self.user1.email = "test-user1@example.com"
            self.user1.password = md5(self.user1.username + "password").hexdigest()

            p2 = Post()
            p2.fingerprint = "1"*32
            p2.tags.append(Tag.get_or_create(u"test-tag"))
            p2.tags.append(Tag.get_or_create(u"bacon"))

            self.user1.posts.append(p2)

            DBSession.add(self.user1)

            # a different user
            self.user2 = User()
            self.user2.username = u"test-user2"
            self.user2.category = "user"
            self.user2.email = "test-user2@example.com"
            self.user2.password = md5(self.user2.username + "password").hexdigest()
            DBSession.add(self.user2)

            wp1 = WikiPage()
            wp1.user = self.user0
            wp1.title = "index"
            wp1.body = "This is the default wiki index page"
            DBSession.add(wp1)

            wp2 = WikiPage()
            wp2.user = self.user0
            wp2.title = "wiki:template"
            wp2.body = "This is the default wiki template page"
            DBSession.add(wp2)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

        cache.slow = cache.make_region()
        cache.fast = cache.make_region()
