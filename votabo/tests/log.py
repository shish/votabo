from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.log import log_list

from votabo.models import (
    DBSession,
    LogEvent,
    )


class test_log_list_empty(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = log_list(request)
        del info["logs"]
        del info["pager"]
        self.assertDictEqual(info, {})

class test_log_list(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        DBSession.add(LogEvent(section=u"sect1", username=u"test-admin", address=u"0.0.0.0", priority=0, message=u"test message 1"))
        DBSession.add(LogEvent(section=u"sect1", username=u"test-client", address=u"0.0.0.0", priority=0, message=u"test message 2"))
        DBSession.add(LogEvent(section=u"sect1", username=u"test-client", address=u"0.0.0.0", priority=0, message=u"test message 3"))

    def test_basic(self):
        request = testing.DummyRequest()
        info = log_list(request)
        self.assertEqual(3, len(info["logs"]))

    def test_username(self):
        request = testing.DummyRequest(GET={"username": u"Test-Client"})
        info = log_list(request)
        self.assertEqual(2, len(info["logs"]))

    def test_message(self):
        request = testing.DummyRequest(GET={"message": u"test"})
        info = log_list(request)
        self.assertEqual(3, len(info["logs"]))

    def test_address(self):
        request = testing.DummyRequest(GET={"address": "0.0.0.0"})
        info = log_list(request)
        self.assertEqual(3, len(info["logs"]))

    def test_module(self):
        request = testing.DummyRequest(GET={"module": "sect1"})
        info = log_list(request)
        self.assertEqual(3, len(info["logs"]))
