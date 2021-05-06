from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutPagesTests(TestCase):
    """The class tests the About application."""
    @classmethod
    def setUpClass(cls):
        """Creating a test object."""
        super().setUpClass()
        cls.templates_urls_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/'
        }
        cls.templates_urlnames_names = {
            'about/author.html': 'about:author',
            'about/tech.html': 'about:tech'
        }

    def setUp(self):
        """Setting the data for testing."""
        self.guest_client = Client()

    def test_url_guest_client(self):
        """The function checks whether the application pages are available
        to an unauthorized user."""
        for value in AboutPagesTests.templates_urls_names.values():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_use_correct_template(self):
        """The function checks whether the expected templates are applied
        to the application."""
        for template, address in AboutPagesTests.templates_urls_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_page_use_correct_template(self):
        """The function checks that the correct template is applied
        to the page by name."""
        for template, name in AboutPagesTests.templates_urlnames_names.items():
            with self.subTest(name=name):
                response = self.guest_client.get(reverse(name))
                self.assertTemplateUsed(response, template)
