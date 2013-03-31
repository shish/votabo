from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from votabo.models import DBSession, Post, Tag, Comment
from votabo.tests import VotaboTest
from votabo.views.comment import comment_list, comment_create, comment_delete

class TestList(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        DBSession.add(self.user0)

        p1 = Post()
        p1.fingerprint = "5"*32
        p1.tags.append(Tag.get_or_create(u"test-tag"))

        p1.comments.append(Comment(self.user0, "0.0.0.0", u"Comment X"))
        p1.comments.append(Comment(self.user1, "0.0.0.0", u"Comment Y"))
        p1.comments.append(Comment(self.user0, "0.0.0.0", u"Comment Z"))

        p2 = Post()
        p2.fingerprint = "6"*32
        p2.tags.append(Tag.get_or_create(u"test-tag"))

        p3 = Post()
        p3.fingerprint = "7"*32
        p3.tags.append(Tag.get_or_create(u"test-tag"))

        p3.comments.append(Comment(self.user0, "0.0.0.0", u"First comment"))
        p3.comments.append(Comment(self.user1, "0.0.0.0", u"Another comment"))
        p3.comments.append(Comment(self.user2, "0.0.0.0", u"Third comment"))

        self.user0.posts.append(p1)
        self.user0.posts.append(p2)
        self.user0.posts.append(p3)

    def test(self):
        request = testing.DummyRequest()
        info = comment_list(request)
        del info["comments"]
        del info["pager"]
        self.assertDictEqual(info, {})


class TestCreate(VotaboTest):
    def setUp(self):
        VotaboTest.setUp(self)
        DBSession.add(self.user0)
        self.post = self.user0.posts[0]

    def test_valid(self):
        request = testing.DummyRequest(user=self.user1, remote_addr="0.0.0.0", method="POST", POST={"post_id": self.post.id, "comment": u"a new comment is here"})
        comment_create(request)
        cs = [comment.body for comment in self.post.comments]
        self.assertIn(u"a new comment is here", cs)

    def test_short(self):
        request = testing.DummyRequest(user=self.user1, remote_addr="0.0.0.0", method="POST", POST={"post_id": self.post.id, "comment": u""})
        info = comment_create(request)
        self.assertIn("comment", info["form"].form.errors)

    def test_long(self):
        request = testing.DummyRequest(user=self.user1, remote_addr="0.0.0.0", method="POST", POST={"post_id": self.post.id, "comment": u"x"*9001})
        info = comment_create(request)
        self.assertIn("comment", info["form"].form.errors)

    def test_white(self):
        request = testing.DummyRequest(user=self.user1, remote_addr="0.0.0.0", method="POST", POST={"post_id": self.post.id, "comment": u"        "})
        info = comment_create(request)
        self.assertIn("comment", info["form"].form.errors)


class TestDelete(VotaboTest):
    def test(self):
        DBSession.add(self.user0)
        comment = Comment(self.user0, "0.0.0.0", u"First comment")
        self.user0.posts[0].comments.append(comment)
        DBSession.flush()

        info = comment_delete(testing.DummyRequest(matchdict={"id": comment.id}))
        self.assertIsInstance(info, HTTPFound)
