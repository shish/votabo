from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.log import log_list


class Test_log_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = log_list(request)
        del info["logs"]
        del info["pager"]
        self.assertDictEqual(info, {})

