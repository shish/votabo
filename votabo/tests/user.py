from pyramid import testing
from pyramid.exceptions import NotFound
from votabo.tests import VotaboTest
from votabo.views.user import user_read, user_update, user_list, PasswordChangeException, UserSettingsException
from votabo.models import (
    DBSession,
    User
)


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

    def test_posts_on(self):
        request = testing.DummyRequest(GET={"posts": "on"})
        info = user_list(request)
        self.assertNotIn(User.by_name(u"test-user1"), info["users"])
        self.assertNotIn(User.by_name(u"test-admin"), info["users"])

    def test_posts_num(self):
        request = testing.DummyRequest(GET={"posts": "0"})
        info = user_list(request)
        self.assertIn(User.by_name(u"test-user1"), info["users"])
        self.assertIn(User.by_name(u"test-admin"), info["users"])

    def test_comments_on(self):
        request = testing.DummyRequest(GET={"comments": "on"})
        info = user_list(request)
        self.assertNotIn(User.by_name(u"test-user1"), info["users"])
        self.assertNotIn(User.by_name(u"test-admin"), info["users"])

    def test_comments_num(self):
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

    def test_404(self):
        request = testing.DummyRequest(matchdict={"name": u"non-exister"})
        self.assertRaises(NotFound, user_read, request)


class test_user_update(VotaboTest):
    def test_self_pass_ok(self):
        DBSession.add(self.user1)
        request = testing.DummyRequest(
            referrer="/",
            user=self.user1,
            matchdict={"name": u"_self"},
            POST={
                "current_password": "password",
                "email": "changed@changed.com",
            }
        )
        info = user_update(request)
        self.assertEqual(self.user1.email, "changed@changed.com")

    def test_self_pass_missing(self):
        DBSession.add(self.user1)
        request = testing.DummyRequest(
            referrer="/",
            user=self.user1,
            matchdict={"name": u"_self"},
            POST={
                "email": "changed@changed.com",
            }
        )
        self.assertRaises(UserSettingsException, user_update, request)

    def test_self_pass_bad(self):
        DBSession.add(self.user1)
        request = testing.DummyRequest(
            referrer="/",
            user=self.user1,
            matchdict={"name": u"_self"},
            POST={
                "current_password": "fdgsdgrfsdfg",
                "email": "changed@changed.com",
            }
        )
        self.assertRaises(UserSettingsException, user_update, request)

    def test_password_ok_other(self):
        DBSession.add(self.user1)
        original_password = self.user1.password

        request = testing.DummyRequest(
            referrer="/",
            matchdict={"name": u"test-user1"},
            POST={
                "new_password_1": "asdf1234",
                "new_password_2": "asdf1234",
            }
        )
        info = user_update(request)

        self.assertNotEqual(self.user1.password, original_password)

    def test_password_ok_self(self):
        DBSession.add(self.user1)
        DBSession.add(self.user2)
        original_password1 = self.user1.password
        original_password2 = self.user2.password

        request = testing.DummyRequest(
            referrer="/",
            user=self.user2,
            matchdict={"name": u"_self"},
            POST={
                "current_password": "password",
                "new_password_1": "asdf1234",
                "new_password_2": "asdf1234",
            }
        )
        info = user_update(request)

        self.assertEqual(self.user1.password, original_password1)
        self.assertNotEqual(self.user2.password, original_password2)

    def test_password_weak(self):
        DBSession.add(self.user1)
        original_password = self.user1.password

        request = testing.DummyRequest(
            referrer="/",
            matchdict={"name": u"test-user1"},
            POST={
                "new_password_1": "asdf",
                "new_password_2": "asdf",
            }
        )
        self.assertRaises(PasswordChangeException, user_update, request)

    def test_password_mismatch(self):
        DBSession.add(self.user1)
        original_password = self.user1.password

        request = testing.DummyRequest(
            referrer="/",
            matchdict={"name": u"test-user1"},
            POST={
                "new_password_1": "asdf1234",
                "new_password_2": "asdf5678",
            }
        )
        self.assertRaises(PasswordChangeException, user_update, request)

    def test_email_set(self):
        DBSession.add(self.user1)
        request = testing.DummyRequest(
            referrer="/",
            matchdict={"name": u"test-user1"},
            POST={"email": "changed@changed.com"}
        )
        info = user_update(request)
        self.assertEqual(self.user1.email, "changed@changed.com")

    def test_email_blank(self):
        DBSession.add(self.user1)
        request = testing.DummyRequest(
            referrer="/",
            matchdict={"name": u"test-user1"},
            POST={"email": ""}
        )
        info = user_update(request)
        self.assertEqual(self.user1.email, None)

