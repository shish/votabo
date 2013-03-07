from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.tag import tag_list


class TestTag(VotaboTest):
    def test_List(self):
        request = testing.DummyRequest()
        info = tag_list(request)
        tags = info["tags"]
        del info["tags"]
        self.assertDictEqual(info, {'starts_with': "a", 'tags_min': 12})
