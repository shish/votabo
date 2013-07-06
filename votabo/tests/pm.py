from pyramid import testing
from pyramid.httpexceptions import HTTPForbidden

from votabo.tests import VotaboTest
from votabo.views.pm import pm_list, pm_create, pm_read, pm_delete
from votabo.models import DBSession, PrivateMessage, User


class test_pm_list(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        self.pm1 = PrivateMessage(user_from=self.user0, user_to=self.user1, subject=u"Hello", message=u"hi there~", is_read=True)
        self.pm2 = PrivateMessage(user_from=self.user1, user_to=self.user0, subject=u"Re: Hello", message=u"ho ho ho", is_read=True)
        self.pm3 = PrivateMessage(user_from=self.user0, user_to=self.user1, subject=u"Re: Hello", message=u"har har")

        DBSession.add_all([self.pm1, self.pm2, self.pm3])

    def test_basic(self):
        request = testing.DummyRequest(user=self.user1)
        info = pm_list(request)
        self.assertIn(self.pm1, info["pms"])
        self.assertIn(self.pm3, info["pms"])


class test_pm_create(VotaboTest):
    def test_valid_send(self):
        DBSession.add(self.user0)
        request = self.mockRequest(user=self.user0, POST={"to": u"test-user1", "subject": u"message~", "message": u"here is some text :3"})
        info = pm_create(request)
        
        info = pm_list(testing.DummyRequest(user=self.user1))
        self.assertIn("message~", [pm.subject for pm in info["pms"]])


class test_pm_read(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        self.pm1 = PrivateMessage(user_from=self.user0, user_to=self.user1, subject=u"Re: Hello", message=u"har har")
        DBSession.add_all([self.pm1])
        DBSession.flush()

    def test_owner_read(self):
        request = testing.DummyRequest(user=self.user1, matchdict={"id": self.pm1.id})
        info = pm_read(request)
        self.assertTrue(self.pm1.is_read)
        self.assertDictEqual(info, {"pm": self.pm1})

    def test_admin_read(self):
        request = testing.DummyRequest(user=self.user0, matchdict={"id": self.pm1.id})
        info = pm_read(request)
        self.assertFalse(self.pm1.is_read)
        self.assertDictEqual(info, {"pm": self.pm1})

    def test_other_read(self):
        DBSession.add(self.user2)  # somehow this ends up not in the session after setUp() o_O
        request = testing.DummyRequest(user=self.user2, matchdict={"id": self.pm1.id})
        self.assertRaises(HTTPForbidden, pm_read, request)


class test_pm_delete(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        self.pm1 = PrivateMessage(user_from=self.user0, user_to=self.user1, subject=u"Re: Hello", message=u"har har")
        DBSession.add_all([self.pm1])
        DBSession.flush()

    def test_owner_delete(self):
        self.assertIn(self.pm1, pm_list(testing.DummyRequest(user=self.user1))["pms"])
        pm_delete(self.mockRequest(user=self.user1, matchdict={"id": self.pm1.id}))
        self.assertNotIn(self.pm1, pm_list(testing.DummyRequest(user=self.user1))["pms"])

    def test_admin_delete(self):
        self.assertIn(self.pm1, pm_list(testing.DummyRequest(user=self.user1))["pms"])
        pm_delete(self.mockRequest(user=self.user0, matchdict={"id": self.pm1.id}))
        self.assertNotIn(self.pm1, pm_list(testing.DummyRequest(user=self.user1))["pms"])

    def test_other_delete(self):
        DBSession.add(self.user2)  # somehow this ends up not in the session after setUp() o_O
        self.assertIn(self.pm1, pm_list(testing.DummyRequest(user=self.user1))["pms"])
        self.assertRaises(HTTPForbidden, pm_delete, self.mockRequest(user=self.user2, matchdict={"id": self.pm1.id}))
        self.assertIn(self.pm1, pm_list(testing.DummyRequest(user=self.user1))["pms"])
