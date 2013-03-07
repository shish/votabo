from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.user import user_read
from votabo.models import User


class TestUser(VotaboTest):
    def test_Read(self):
        request = testing.DummyRequest(matchdict={"name": u"test-admin"})
        info = user_read(request)

        self.assertIsInstance(info["duser"], User)
        del info["duser"]

        self.assertDictEqual(info, {})
