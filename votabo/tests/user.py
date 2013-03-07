from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.user import user_read, user_list
from votabo.models import User


class test_user_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = user_list(request)
        del info["users"]
        del info["pager"]
        self.assertDictEqual(info, {})


class test_user_read(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(matchdict={"name": u"test-admin"})
        info = user_read(request)

        self.assertIsInstance(info["duser"], User)
        del info["duser"]

        self.assertDictEqual(info, {})
