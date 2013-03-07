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

    def test_Post_nonexist(self):
        request = testing.DummyRequest(GET={"q": u"iasdfasdf"})
        info = post_list(request)
        del info["posts"]
        del info["pager"]
        self.assertDictEqual(info, {})
