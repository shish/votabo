from pyramid import testing

from votabo.models import DBSession
from votabo.tests import VotaboTest
from votabo.views.post import post_list, post_read, post_upload


class test_post_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = post_list(request)
        self.assertEqual(2, len(info["posts"]))

    def test_search(self):
        request = testing.DummyRequest(GET={"q": u"test-tag"})
        info = post_list(request)
        self.assertEqual(2, len(info["posts"]))

    def test_search_sort_default(self):
        request = testing.DummyRequest(GET={})
        info = post_list(request)
        self.assertGreater(info["posts"][0].id, info["posts"][1].id)

    def test_search_sort_score(self):
        request = testing.DummyRequest(GET={"q": u"sort:score"})
        info = post_list(request)
        self.assertGreater(info["posts"][0].score, info["posts"][1].score)

    def test_nonexist_tag(self):
        request = testing.DummyRequest(GET={"q": u"iasdfasdf"})
        info = post_list(request)
        del info["posts"]
        del info["pager"]
        self.assertDictEqual(info, {'query': u"iasdfasdf"})


class test_post_read(VotaboTest):
    def test_basic(self):
        DBSession.add(self.user0)
        request = testing.DummyRequest(matchdict={"id": self.user0.posts[0].id})
        info = post_read(request)


class test_upload(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = post_upload(request)
        self.assertDictEqual(info, {})
