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
