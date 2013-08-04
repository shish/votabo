from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.models import UnTag, User
from votabo.tests import VotaboTest
from votabo.views.untag import UnTagExistsException
from votabo.views.untag import untag_create, untag_list, untag_delete

import logging

logger = logging.getLogger(__name__)


_ban = {"tag": u"test_untag", "redirect": u"/wiki/untags"}

class test_untag_create(VotaboTest):
    def test_create_ok(self):
        user = User.by_name(u"test-admin")
        info = untag_create(testing.DummyRequest(POST=_ban, user=user))
        self.assertIsInstance(info, HTTPFound)

        info = untag_list(testing.DummyRequest())
        banned_tags = [untag.tag for untag in info["untags"]]
        self.assertListEqual(["test_untag"], banned_tags)

    def test_create_dupe(self):
        user = User.by_name(u"test-admin")
        info = untag_create(testing.DummyRequest(POST=_ban, user=user))
        self.assertIsInstance(info, HTTPFound)

        user = User.by_name(u"test-admin")
        self.assertRaises(UnTagExistsException, untag_create, testing.DummyRequest(POST=_ban, user=user))

        info = untag_list(testing.DummyRequest())
        banned_tags = [untag.tag for untag in info["untags"]]
        self.assertListEqual(["test_untag"], banned_tags)


class test_untag_list_empty(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = untag_list(request)
        del info["untags"]
        del info["pager"]
        self.assertDictEqual(info, {})


class test_untag_list(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        user = User.by_name(u"test-admin")
        untag_create(testing.DummyRequest(POST={"tag": u"untag_test1", "redirect": u"/wiki/TestX"}, user=user))
        untag_create(testing.DummyRequest(POST={"tag": u"untag_test2", "redirect": u"/wiki/TestY"}, user=user))
        untag_create(testing.DummyRequest(POST={"tag": u"untag_test3", "redirect": u"/wiki/TestY"}, user=user))

    def test_tag_exact(self):
        info = untag_list(testing.DummyRequest(GET={"tag": u"untag_test1"}))
        self.assertEqual(len(info["untags"]), 1)
        self.assertEqual(info["untags"][0].redirect, "/wiki/TestX")

    def test_redirect(self):
        info = untag_list(testing.DummyRequest(GET={"redirect": u"/wiki/TestY"}))
        self.assertEqual(len(info["untags"]), 2)


class test_untag_delete(VotaboTest):
    def test_basic(self):
        user = User.by_name(u"test-admin")
        info = untag_create(testing.DummyRequest(POST=_ban, user=user))
        self.assertIsInstance(info, HTTPFound)

        info = untag_list(testing.DummyRequest())
        banned_tags = [untag.tag for untag in info["untags"]]
        self.assertListEqual(["test_untag"], banned_tags)

        info = untag_delete(testing.DummyRequest(matchdict={"tag": u"test_untag"}, referrer="/"))
        self.assertIsInstance(info, HTTPFound)

        info = untag_list(testing.DummyRequest())
        banned_tags = [untag.tag for untag in info["untags"]]
        self.assertListEqual([], banned_tags)
