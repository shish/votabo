from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.home import home


class TestHome(VotaboTest):
    def test_home(self):
        request = testing.DummyRequest()
        info = home(request)
        self.assertDictEqual(info, {'post_count': 2, 'site_title': None})
