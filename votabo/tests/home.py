from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.home import home


class TestHome(VotaboTest):
    def test_Home(self):
        request = testing.DummyRequest()
        info = home(request)
        self.assertDictEqual(info, {'post_count': 1, 'site_title': None})
