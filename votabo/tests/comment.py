from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.comment import comment_list

class TestComment(VotaboTest):
    def test_Comment(self):
        request = testing.DummyRequest()
        info = comment_list(request)
        del info["comments"]
        del info["pager"]
        self.assertDictEqual(info, {})
