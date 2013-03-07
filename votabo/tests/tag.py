from pyramid import testing
from votabo.tests import VotaboTest
from votabo.views.tag import tag_list, tag_list_xhr


class test_tag_list(VotaboTest):
    def test_basic(self):
        request = testing.DummyRequest()
        info = tag_list(request)
        tags = info["tags"]
        del info["tags"]
        self.assertDictEqual(info, {'starts_with': "a", 'tags_min': 12})

    def test_xhr(self):
        request = testing.DummyRequest()
        info = tag_list_xhr(request)
        tags = info["tags"]
        del info["tags"]
        self.assertDictEqual(info, {'starts_with': "a", 'tags_min': 12})
