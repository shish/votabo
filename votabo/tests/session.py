from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.tests import VotaboTest
from votabo.views.session import session_create, session_delete, SessionException


class test_session(VotaboTest):
    def test_create_ok(self):
        request = testing.DummyRequest(POST={"username": u"test-admin", "password": u"password"})
        info = session_create(request)
        self.assertIsInstance(info, HTTPFound)

    def test_create_bad(self):
        request = testing.DummyRequest(POST={"username": u"test-admin", "password": u"moosdfas"})
        self.assertRaises(SessionException, session_create, request)

    def test_delete(self):
        request = testing.DummyRequest()
        info = session_delete(request)
        self.assertIsInstance(info, HTTPFound)
