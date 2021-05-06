import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class YatubeNewPostTests(TestCase):
    """Test for checking the form for creating a new post."""
    @classmethod
    def setUpClass(cls):
        """Creating a test object."""
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create(username='vsemikin')
        cls.authorized_user = User.objects.create(username='oleg')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user
        )
        cls.post_author = Client()
        cls.post_author.force_login(cls.post.author)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Setting the data for testing."""
        self.authorized_client = Client()
        self.authorized_client.force_login(YatubeNewPostTests.authorized_user)

    def test_form_new_post(self):
        """The function checks the creation of a new record in the database."""
        post_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Новый пост',
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(response.status_code, 200)

    def test_form_post_edit(self):
        """The function checks the change of the corresponding record
        in the database after editing."""
        form_data = {
            'text': 'Отредактированный пост'
        }
        response = YatubeNewPostTests.post_author.post(
            reverse('post_edit', args=('vsemikin', 1)),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.context['post'].text, form_data['text'])
