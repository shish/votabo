from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.user import user_read, user_list
from votabo.models import User


class test_user_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = user_list(request)
        self.assertIn(User.by_name(u"test-user1"), info["users"])
        self.assertIn(User.by_name(u"test-admin"), info["users"])

    def test_id(self):
        request = testing.DummyRequest(GET={"id": User.by_name(u"test-admin").id})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-admin"), info["users"])
        self.assertNotIn(User.by_name(u"test-user1"), info["users"])

    def test_username_exact(self):
        request = testing.DummyRequest(GET={"username": u"test-admin"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-admin"), info["users"])
        self.assertNotIn(User.by_name(u"test-user1"), info["users"])

    def test_username_postfix(self):
        request = testing.DummyRequest(GET={"username": u"admin"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-admin"), info["users"])
        self.assertNotIn(User.by_name(u"test-user1"), info["users"])

    def test_username_prefix(self):
        request = testing.DummyRequest(GET={"username": u"test"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-admin"), info["users"])
        self.assertIn(User.by_name(u"test-user1"), info["users"])

    def test_posts(self):
        request = testing.DummyRequest(GET={"posts": "0"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-user1"), info["users"])
        self.assertIn(User.by_name(u"test-admin"), info["users"])

    def test_comments(self):
        request = testing.DummyRequest(GET={"comments": "0"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-user1"), info["users"])
        self.assertIn(User.by_name(u"test-admin"), info["users"])

    def test_category(self):
        request = testing.DummyRequest(GET={"category": u"admin"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-admin"), info["users"])
        self.assertNotIn(User.by_name(u"test-user1"), info["users"])


class test_user_read(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(matchdict={"name": u"test-admin"})
        info = user_read(request)

        self.assertIsInstance(info["duser"], User)
        del info["duser"]

        self.assertDictEqual(info, {})
