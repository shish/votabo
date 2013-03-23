from mock import MagicMock

from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.tests import VotaboTest
from votabo.views.wiki import wiki_read, wiki_update, wiki_delete


class test_read(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(matchdict={"title": u"index"})
        info = wiki_read(request)
        self.assertEqual(info["page"].title, "index")
        self.assertEqual(info["page"].body, "This is the default wiki index page")

    def test_unknown(self):
        request = testing.DummyRequest(matchdict={"title": u"page-that-does-not-exist"})
        info = wiki_read(request)
        self.assertIsInstance(info, HTTPFound)


class test_update(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(method="POST", user=self.user0, matchdict={"title": u"index"}, POST={"body": u"a new index"})
        info = wiki_update(request)
        self.assertIsInstance(info, HTTPFound)
        # self.assertEqual(request.session.flash.call_count, 1)

    def test_new(self):
        request = testing.DummyRequest(method="POST", user=self.user0, matchdict={"title": u"some-new-page"}, POST={"body": u"a new page body"})
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
