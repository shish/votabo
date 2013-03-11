from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.tests import VotaboTest
from votabo.views.alias import AliasExistsException, AliasLoopException
from votabo.views.alias import alias_create, alias_list, alias_delete


class TestAliasCreate(VotaboTest):
    def test_Create_ok(self):
        info = alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))
        self.assertIsInstance(info, HTTPFound)

        info = alias_list(testing.DummyRequest())
        aliases = [alias.oldtag for alias in info["aliases"]]
        self.assertIn(u"Bender", aliases)

    def test_Create_dupe(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))

        request = testing.DummyRequest(POST={"oldtag": u"bender", "newtag": u"bender_bending_rodriguez"})
        self.assertRaises(AliasExistsException, alias_create, request)

    def test_Create_loop(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))

        request = testing.DummyRequest(POST={"oldtag": u"bender_bending_rodriguez", "newtag": u"bender"})
        self.assertRaises(AliasLoopException, alias_create, request)


class TestAliasList(VotaboTest):
    def test_AliasList_blank(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))
        alias_create(testing.DummyRequest(POST={"oldtag": u"Obama", "newtag": u"Barack_Obama"}))

        info = alias_list(testing.DummyRequest())
        aliases = [alias.oldtag for alias in info["aliases"]]
        self.assertIn(u"Bender", aliases)

    def test_AliasList_oldtag(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))
        alias_create(testing.DummyRequest(POST={"oldtag": u"Obama", "newtag": u"Barack_Obama"}))

        info = alias_list(testing.DummyRequest(GET={"oldtag": u"bender"}))
        aliases = [alias.oldtag for alias in info["aliases"]]
        self.assertListEqual([u"Bender"], aliases)

    def test_AliasList_newtag(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))
        alias_create(testing.DummyRequest(POST={"oldtag": u"Obama", "newtag": u"Barack_Obama"}))

        info = alias_list(testing.DummyRequest(GET={"newtag": u"barack_obama"}))
        aliases = [alias.oldtag for alias in info["aliases"]]
        self.assertListEqual([u"Obama"], aliases)

    def test_AliasList_noResult(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))
        alias_create(testing.DummyRequest(POST={"oldtag": u"Obama", "newtag": u"Barack_Obama"}))

        info = alias_list(testing.DummyRequest(GET={"newtag": u"cats"}))
        aliases = [alias.oldtag for alias in info["aliases"]]
        self.assertListEqual([], aliases)


class Test_Alias_Delete(VotaboTest):
    def test_AliasDelete(self):
        alias_create(testing.DummyRequest(POST={"oldtag": u"Bender", "newtag": u"Bender_Bending_Rodriguez"}))

        info = alias_delete(testing.DummyRequest(matchdict={"id": u"Bender"}))
        self.assertIsInstance(info, HTTPFound)

        info = alias_list(testing.DummyRequest())
        aliases = [alias.oldtag for alias in info["aliases"]]
        self.assertListEqual([], aliases)
