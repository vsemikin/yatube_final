from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class YatubeURLTests(TestCase):
    """The class tests the correctness of URLs
    (availability, templates, permissions)."""
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
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )
        cls.templates_url_names_public = {
            'posts/index.html': '',
            'posts/group.html': f'/group/{cls.group.slug}/',
            'posts/profile.html': f'/{cls.user}/',
            'posts/post.html': f'/{cls.user}/{cls.post.id}/'
        }
        cls.post_new_url = '/new/'
        cls.post_edit_url = f'/{cls.user}/{cls.post.id}/edit/'
        cls.templates_url_names_private = (
            ('posts/new.html', cls.post_new_url),
            ('posts/new.html', cls.post_edit_url),
        )

    def setUp(self):
        """Setting the data for testing."""
        self.guest_client = Client()
        self.user = User.objects.create(username='oleg')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_author = Client()
        self.post_author.force_login(YatubeURLTests.post.author)

    def test_server_return_404_code(self):
        """The function checks if the server returns a 404 code
        if the page is not found."""
        response = self.guest_client.get('/non-existent/page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_public_url_guest_client(self):
        """The function checks the availability of public pages for an
        anonymous user."""
        for value in YatubeURLTests.templates_url_names_public.values():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_url_guest_client(self):
        """The function checks the availability of private pages for an
        anonymous user and a user who is not the author of the post."""
        for _, address in YatubeURLTests.templates_url_names_private:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.guest_client.get(
            YatubeURLTests.post_new_url, follow=True
        )
        post_new_url = YatubeURLTests.post_new_url
        self.assertRedirects(response, f'/auth/login/?next={post_new_url}')
        response = self.guest_client.get(
            YatubeURLTests.post_edit_url, follow=True
        )
        post_edit_url = YatubeURLTests.post_edit_url
        self.assertRedirects(response, f'/auth/login/?next={post_edit_url}')

    def test_public_url_authorized_client(self):
        """The function checks the availability of pages for the
        registered user."""
        response = self.authorized_client.get(YatubeURLTests.post_new_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.get(YatubeURLTests.post_edit_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.authorized_client.get(
            YatubeURLTests.post_edit_url, follow=True
        )
        self.assertRedirects(
            response, '/vsemikin/1/'
        )

    def test_url_authorized_client_post_author(self):
        """The function checks the availability of pages for the
        registered user(author of the post)."""
        response = self.post_author.get(YatubeURLTests.post_edit_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_use_correct_template_public_pages(self):
        """The function checks whether the address matches
        the page template."""
        for template, address in (
            YatubeURLTests.templates_url_names_public.items()
        ):
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_use_correct_template_private_pages(self):
        """The function checks whether the address matches
        the page template."""
        for template, address in YatubeURLTests.templates_url_names_private:
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertTemplateUsed(response, template)
