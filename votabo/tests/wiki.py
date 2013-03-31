from mock import MagicMock

from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.models import DBSession, WikiPage
from votabo.tests import VotaboTest
from votabo.views.wiki import wiki_read, wiki_update, wiki_delete


class test_read(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        wp1 = WikiPage()
        wp1.user = self.user0
        wp1.title = u"index"
        wp1.revision = 2
        wp1.body = u"This is the default wiki index page, v2"
        DBSession.add(wp1)

    def test_basic(self):
        request = testing.DummyRequest(matchdict={"title": u"index"})
        info = wiki_read(request)
        self.assertEqual(info["page"].title, "index")
        self.assertEqual(info["page"].revision, 2)
        self.assertEqual(info["page"].body, "This is the default wiki index page, v2")

    def test_unknown(self):
        request = testing.DummyRequest(matchdict={"title": u"page-that-does-not-exist"})
        info = wiki_read(request)
        self.assertIsInstance(info, HTTPFound)

    def test_version(self):
        request = testing.DummyRequest(matchdict={"title": u"index"}, GET={"revision": u"1"})
        info = wiki_read(request)
        self.assertIsInstance(info, dict)
        self.assertEqual(info["page"].title, "index")
        self.assertEqual(info["page"].revision, 1)
        self.assertEqual(info["page"].body, "This is the default wiki index page")


class test_update(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(method="PUT", user=self.user0, matchdict={"title": u"index"}, params={"title": u"index", "body": u"a new index"})
        info = wiki_update(request)
        self.assertIsInstance(info, HTTPFound)
        # self.assertEqual(request.session.flash.call_count, 1)

    def test_new(self):
        request = testing.DummyRequest(method="PUT", user=self.user0, matchdict={"title": u"some-new-page"}, params={"title": u"some-new-page", "body": u"a new page body"})
        info = wiki_update(request)
        self.assertIsInstance(info, HTTPFound)


class test_delete(VotaboTest):
    def test_exist(self):
        request = testing.DummyRequest(matchdict={"title": u"index"})
        info = wiki_delete(request)
        self.assertIsInstance(info, HTTPFound)
        # self.assertEqual(request.session.flash.call_count, 1)

        request = testing.DummyRequest(matchdict={"title": u"index"})
        info = wiki_read(request)
        self.assertIsInstance(info, HTTPFound)

    def test_notexist(self):
        request = testing.DummyRequest(matchdict={"title": u"page-that-does-not-exist"})
        info = wiki_delete(request)
        self.assertIsInstance(info, HTTPFound)
        # self.assertEqual(request.session.flash.call_count, 0)
