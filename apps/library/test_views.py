from django.test import TestCase

from .models import Author, Book, Genre
from ..geotracking.utils import Utils
from ..geotracking.models import Visitor


class LibraryViews(TestCase):

    # this client IP should be random, in order to avoid
    # any blocking request from ipinfo.io...
    client_ip = Utils.get_random_public_ip()

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name="John", last_name="Doe")

    def test_get_author(self):
        self.client.defaults['REMOTE_ADDR'] = LibraryViews.client_ip
        response = self.client.get(f'/apps/library/authors/{self.author.id}/')
        self.assertEqual(response.status_code, 200)
        visitor = Visitor.objects.filter(ip=LibraryViews.client_ip)
        self.assertTrue(visitor)
        self.assertEqual(visitor[0].ip, str(LibraryViews.client_ip))
        response = self.client.get(f'/apps/library/authors/{self.author.id}/')
        visitor[0].refresh_from_db()
        self.assertEqual(visitor[0].amount_of_requests, 2)
