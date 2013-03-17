from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.models import User
from votabo.tests import VotaboTest
from votabo.views.ipban import IPBanExistsException
from votabo.views.ipban import ipban_create, ipban_list, ipban_delete

import logging

logger = logging.getLogger(__name__)


_ban = {"ip": u"1.2.3.4", "reason": u"Test Ban", "until": u"+3 weeks"}

class test_ipban_create(VotaboTest):
    def test_Create_ok(self):
        user = User.by_name(u"test-admin")
        info = ipban_create(testing.DummyRequest(POST=_ban, user=user))
        self.assertIsInstance(info, HTTPFound)

        info = ipban_list(testing.DummyRequest())
        banned_ips = [ipban.ip for ipban in info["ipbans"]]
        self.assertListEqual(["1.2.3.4"], banned_ips)

    def test_Create_dupe(self):
        user = User.by_name(u"test-admin")
        info = ipban_create(testing.DummyRequest(POST=_ban, user=user))
        self.assertIsInstance(info, HTTPFound)

        user = User.by_name(u"test-admin")
        self.assertRaises(IPBanExistsException, ipban_create, testing.DummyRequest(POST=_ban, user=user))

        info = ipban_list(testing.DummyRequest())
        banned_ips = [ipban.ip for ipban in info["ipbans"]]
        self.assertListEqual(["1.2.3.4"], banned_ips)


class test_ipban_list_empty(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = ipban_list(request)
        del info["ipbans"]
        del info["pager"]
        self.assertDictEqual(info, {})


class test_ipban_list(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        user = User.by_name(u"test-admin")
        ipban_create(testing.DummyRequest(POST={"ip": u"1.2.3.4", "reason": u"TestX BanX", "until": u"+3 weeks"}, user=user))
        ipban_create(testing.DummyRequest(POST={"ip": u"1.2.3.5", "reason": u"TestY BanX", "until": u"+3 weeks"}, user=user))
        ipban_create(testing.DummyRequest(POST={"ip": u"6.2.3.4", "reason": u"TestY BanY", "until": u"+3 weeks"}, user=user))

    def test_ip_exact(self):
        info = ipban_list(testing.DummyRequest(GET={"ip": u"1.2.3.4"}))
        self.assertEqual(len(info["ipbans"]), 1)
        self.assertEqual(info["ipbans"][0].reason, "TestX BanX")

#    # requires postgres
#    def test_ip_net(self):
#        info = ipban_list(testing.DummyRequest(GET={"ip": u"1.2.3.0/24"}))
#        self.assertEqual(len(info["ipbans"]), 2)
#
#        info = ipban_list(testing.DummyRequest(GET={"ip": u"6.2.3.0/24"}))
#        self.assertEqual(len(info["ipbans"]), 1)

    def test_banner(self):
        info = ipban_list(testing.DummyRequest(GET={"banner": u"test-admin"}))
        self.assertEqual(len(info["ipbans"]), 3)

    def test_reason(self):
        info = ipban_list(testing.DummyRequest(GET={"reason": u"testy"}))
        self.assertEqual(len(info["ipbans"]), 2)


class test_ipban_delete(VotaboTest):
    def test_basic(self):
        user = User.by_name(u"test-admin")
        info = ipban_create(testing.DummyRequest(POST=_ban, user=user))
        self.assertIsInstance(info, HTTPFound)
        ban_id = info.headers["X-VTB-Ban-ID"]

        logger.info("Got ban ID: %r" % ban_id)

        info = ipban_delete(testing.DummyRequest(matchdict={"id": ban_id}))
        self.assertIsInstance(info, HTTPFound)

        info = ipban_list(testing.DummyRequest())
        banned_ips = [ipban.ip for ipban in info["ipbans"]]
        self.assertListEqual([], banned_ips)
