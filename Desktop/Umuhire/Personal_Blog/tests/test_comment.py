
import unittest
from app.models import Comment,User,Blog
from app import db



class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_anne = User(username = 'anuarithe',password = 'aaaaaa', email = 'a@gmail.com')
        self.new_blog = Blog(id=1,blog_title='Music',blog_content='music is part of life',user = self.user_anne)
        self.new_comment = Comment(id=1,comment='publish comment',user=self.user_anne,blog=self.new_blog)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'publish comment')
        self.assertEquals(self.new_comment.user,self.user_anne)
        self.assertEquals(self.new_comment.blog,self.new_blog)
