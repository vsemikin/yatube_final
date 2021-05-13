import shutil
import tempfile
from http import HTTPStatus

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(dir=settings.BASE_DIR))
class YatubePagesTests(TestCase):
    """The class tests the correctness of template names and
    the transmission of the correct context."""
    @classmethod
    def setUpClass(cls):
        """Creating a test object."""
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.user = User.objects.create(username='vsemikin')
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded
        )
        cls.new_group = Group.objects.create(title='Тест', slug='test')
        cls.templates_pages_names = {
            'posts/index.html': reverse('index'),
            'posts/group.html': (
                reverse('group_posts', kwargs={'slug': 'test-slug'})
            ),
            'posts/new.html': reverse('new_post'),
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        """Setting the data for testing."""
        self.post_author = Client()
        self.post_author.force_login(YatubePagesTests.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(YatubePagesTests.user)

    def check_correct_post_in_context(self, post):
        """The function checks to meet the expectations of the
        passed context."""
        self.assertEqual(post.text, YatubePagesTests.post.text)
        self.assertEqual(
            post.author.username, YatubePagesTests.post.author.username
        )
        self.assertEqual(post.group.title, YatubePagesTests.post.group.title)
        self.assertEqual(post.image, YatubePagesTests.post.image)

    def test_pages_uses_correct_template_name(self):
        """The function tests which template will be called
        when accessing the view classes."""
        for template, reverse_name in (
            YatubePagesTests.templates_pages_names.items()
        ):
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_shows_correct_context(self):
        """The function tests whether the context dictionary passed to the
        home page template when called meets the expectations."""
        response = self.authorized_client.get(reverse('index'))
        post = response.context['page'][0]
        self.check_correct_post_in_context(post)

    def test_group_page_shows_correct_context(self):
        """The function tests whether the context dictionary passed to the
        group page template when called meets the expectations."""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'})
        )
        group = response.context['group']
        self.assertEqual(group.title, YatubePagesTests.group.title)
        self.assertEqual(group.slug, YatubePagesTests.group.slug)
        self.assertEqual(group.description, YatubePagesTests.group.description)
        post = response.context['page'][0]
        self.check_correct_post_in_context(post)

    def test_new_post_page_shows_correct_context(self):
        """The function tests whether the context dictionary
        passed to the template of the post creation page meets
        the expectations when called."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_post_specify_group_home_page(self):
        """The function tests the appearance of a post on the main page
        if you specify a group when creating it."""
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context['page']), 1)

    def test_create_post_specify_group_group_page(self):
        """The function tests the appearance of the post on the group page
        if you specify the group when creating it."""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(len(response.context['page']), 1)

    def test_create_post_not_included_group(self):
        """The function tests the appearance of a post on the page of another group
        if you specify the group when creating it."""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test'})
        )
        self.assertNotEqual(len(response.context['page']), 1)

    def test_post_page_edit_shows_correct_context(self):
        """The function checks the content of the context dictionary passed
        to the template of the post editing page."""
        response = self.post_author.get(
            reverse('post_edit', args=(
                YatubePagesTests.post.author.username,
                YatubePagesTests.post.id
            )
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_page_shows_correct_context(self):
        """The function checks the contents of the passed context dictionary
        to the author's profile page template."""
        response = self.authorized_client.get(
            reverse('profile', args=[YatubePagesTests.post.author.username])
        )
        self.assertEqual(
            response.context['author'].username,
            YatubePagesTests.post.author.username
        )
        self.assertEqual(
            response.context['author'].posts.count(), 1
        )
        post = response.context['page'][0]
        self.check_correct_post_in_context(post)

    def test_post_page_shows_correct_context(self):
        """The function checks the content of the passed context dictionary
        to the page template of an individual author's post."""
        response = self.authorized_client.get(
            reverse('post_view', args=(
                YatubePagesTests.post.author.username,
                YatubePagesTests.post.id
            )
            )
        )
        post = response.context['post']
        self.check_correct_post_in_context(post)


class PaginatorViewsTest(TestCase):
    """The class tests how Paginator works."""
    @classmethod
    def setUpClass(cls):
        """Creating a test objects."""
        super().setUpClass()
        items = range(13)
        for item in items:
            Post.objects.create(
                text=f'Тестовый текст{item}',
                author=User.objects.create(username=f'user{item}')
            )

    def test_first_page_contains_ten_records(self):
        """The function checks that 10 entries are displayed
        on the first page."""
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        """The function checks that 3 entries are displayed
        on the second page."""
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)


class FollowAndCommentViewsTest(TestCase):
    """The class checks the operation of the subscriptions and
    comments system."""
    @classmethod
    def setUpClass(cls):
        """Creating a test object."""
        super().setUpClass()
        cls.user = User.objects.create(username='vsemikin')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def setUp(self):
        """Setting the data for testing."""
        self.guest_client = Client()
        self.user = User.objects.create(username='oleg')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.another_user = User.objects.create(username='galina')
        self.another_authorized_client = Client()
        self.another_authorized_client.force_login(self.another_user)
        self.authorized_client.get(
            reverse('profile_follow', args=[FollowAndCommentViewsTest.user])
        )

    def test_authorized_user_subscribe(self):
        """The function checks whether an authorized user can subscribe to other users
        and remove them from subscriptions."""
        self.assertEqual(FollowAndCommentViewsTest.user.following.count(), 1)

    def test_authorized_user_remove_subscriptions(self):
        """The function checks whether an authorized user can subscribe to other users
        and remove them from subscriptions."""
        self.authorized_client.get(
            reverse('profile_unfollow', args=[FollowAndCommentViewsTest.user])
        )
        self.assertEqual(FollowAndCommentViewsTest.user.following.count(), 0)

    def test_new_user_entry_appears_in_following(self):
        """The function checks whether a new user entry appears in the feed
        of those who are subscribed to it and does not appear in the feed
        of those who are not subscribed to it."""
        response = self.authorized_client.get(reverse('follow_index'))
        self.assertEqual(len(response.context.get('page').object_list), 1)

    def test_new_user_entry_appears_in_not_following(self):
        """The function checks whether a new user entry appears in the feed
        of those who are subscribed to it and does not appear in the feed
        of those who are not subscribed to it."""
        response = self.another_authorized_client.get(reverse('follow_index'))
        self.assertEqual(len(response.context.get('page').object_list), 0)

    def test_authorized_user_can_comment_on_posts(self):
        """The function checks that only an authorized user can comment
        on posts."""
        response = self.authorized_client.get(
            reverse('add_comment', args=(
                FollowAndCommentViewsTest.user,
                FollowAndCommentViewsTest.post.id
            )
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_guest_user_can_not_comment_on_posts(self):
        """The function checks that only an authorized user can comment
        on posts."""
        response = self.guest_client.get(
            reverse('add_comment', args=(
                FollowAndCommentViewsTest.user,
                FollowAndCommentViewsTest.post.id
            )
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
