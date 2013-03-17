from pyramid import testing
from pyramid.httpexceptions import HTTPForbidden

from votabo.tests import VotaboTest
from votabo.views.pm import pm_read, pm_list
from votabo.models import DBSession, PrivateMessage, User


class test_pm_list(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        self.u1 = User.by_name(u"test-admin")
        self.u2 = User.by_name(u"test-user")

        self.pm1 = PrivateMessage(user_from=self.u1, user_to=self.u2, subject=u"Hello", message=u"hi there~", is_read=True)
        self.pm2 = PrivateMessage(user_from=self.u2, user_to=self.u1, subject=u"Re: Hello", message=u"ho ho ho", is_read=True)
        self.pm3 = PrivateMessage(user_from=self.u1, user_to=self.u2, subject=u"Re: Hello", message=u"har har")

        DBSession.add_all([self.pm1, self.pm2, self.pm3])

    def test_basic(self):
        request = testing.DummyRequest(user=self.u2)
        info = pm_list(request)
        self.assertIn(self.pm1, info["pms"])
        self.assertIn(self.pm3, info["pms"])


class test_pm_read(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        self.u1 = User.by_name(u"test-admin")
        self.u2 = User.by_name(u"test-user")
        self.u3 = User.by_name(u"test-user2")
        self.pm1 = PrivateMessage(user_from=self.u1, user_to=self.u2, subject=u"Re: Hello", message=u"har har")
        DBSession.add_all([self.pm1])
        DBSession.flush()

    def test_owner_read(self):
        request = testing.DummyRequest(user=self.u2, matchdict={"id": self.pm1.id})
        info = pm_read(request)
        self.assertTrue(self.pm1.is_read)
        self.assertDictEqual(info, {"pm": self.pm1})

    def test_admin_read(self):
        request = testing.DummyRequest(user=self.u1, matchdict={"id": self.pm1.id})
        info = pm_read(request)
        self.assertFalse(self.pm1.is_read)
        self.assertDictEqual(info, {"pm": self.pm1})

    def test_other_read(self):
        request = testing.DummyRequest(user=self.u3, matchdict={"id": self.pm1.id})
        self.assertRaises(HTTPForbidden, pm_read, request)