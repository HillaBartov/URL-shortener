from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import URL
from .views import unique_slugify


class URLListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create short url to a full url
        url = URL.objects.create(
            url='https://www.pcentra.com/',
            slug=unique_slugify(),
        )
        url.save()

    def test_view_create_short_url(self):
        data = {
            'url': 'https://www.pcentra.com/'
        }
        response = self.client.post(reverse("create"), data)
        self.assertEqual(response.status_code, 201)

    def test_view_url_exists_for_created_short(self):
        url = get_object_or_404(URL, url='https://www.pcentra.com/')
        response = self.client.get(reverse("short", args=(url.slug,)))
        self.assertEqual(response.status_code, 302)

    def test_view_non_existing_short_url(self):
        slug = unique_slugify()
        response = self.client.get(reverse("short", args=(slug,)))
        self.assertEqual(response.status_code, 404)
