from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    """Test class for the post model."""
    @classmethod
    def setUpClass(cls):
        """The function creates an object of the post class."""
        super().setUpClass()
        cls.user = User.objects.create()
        cls.post = Post.objects.create(
            text='Этот текст поста больше 15-ти символов',
            author=cls.user
        )

    def test_text_fild(self):
        """The function checks the value of the __str__
        field in the model object."""
        post = PostModelTest.post
        expected = post.text
        self.assertEqual(str(post), expected)


class GroupModelTest(TestCase):
    """Test class for the group model."""
    @classmethod
    def setUpClass(cls):
        """The function creates an object of the group class."""
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый текст'
        )

    def test_title_fild(self):
        """The function checks the value of the __str__
        field in the model object."""
        group = GroupModelTest.group
        expected = group.title
        self.assertEqual(str(group), expected)
