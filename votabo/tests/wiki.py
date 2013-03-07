from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.wiki import wiki_read


class test_wiki_read(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest(matchdict={"title": u"test"})
        info = wiki_read(request)
        del info["index"]
        del info["page"]
        self.assertDictEqual(info, {})
