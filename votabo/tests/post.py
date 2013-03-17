from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.post import post_list


class test_post_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = post_list(request)
        self.assertEqual(2, len(info["posts"]))

    def test_search(self):
        request = testing.DummyRequest(GET={"q": u"test-tag"})
        info = post_list(request)
        self.assertEqual(2, len(info["posts"]))

    def test_nonexist_tag(self):
        request = testing.DummyRequest(GET={"q": u"iasdfasdf"})
        info = post_list(request)
        del info["posts"]
        del info["pager"]
        self.assertDictEqual(info, {})


class test_post_view(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(GET={"q": u"iasdfasdf"})
        info = post_list(request)
        del info["posts"]
        del info["pager"]
        self.assertDictEqual(info, {})
