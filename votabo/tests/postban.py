from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.postban import postban_list


class test_postban_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = postban_list(request)
        del info["postbans"]
        del info["pager"]
        self.assertDictEqual(info, {})

    def test_fingerprint(self):
        request = testing.DummyRequest(GET={"fingerprint": "0"*32})
        info = postban_list(request)
        del info["postbans"]
        del info["pager"]
        self.assertDictEqual(info, {})

    def test_reason(self):
        request = testing.DummyRequest(GET={"reason": u"test ban"})
        info = postban_list(request)
        del info["postbans"]
        del info["pager"]
        self.assertDictEqual(info, {})
