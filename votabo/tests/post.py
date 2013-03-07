from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.post import post_list


class TestPost(VotaboTest):
    def test_Post(self):
        request = testing.DummyRequest()
        info = post_list(request)
        del info["posts"]
        del info["pager"]
        self.assertDictEqual(info, {})
