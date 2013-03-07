from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.ipban import ipban_list


class Test_ipban_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = ipban_list(request)
        del info["ipbans"]
        del info["pager"]
        self.assertDictEqual(info, {})

