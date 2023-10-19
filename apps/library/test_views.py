from django.conf import settings
from django.test import TestCase

from .models import Author, Book, Genre
from ..geotracking.utils import Utils
from ..geotracking.models import Visitor


class LibraryViews(TestCase):

    # Client IP should be random, in order to avoid any request blockers from ipinfo.io.
    client_ip = Utils.get_random_public_ip()

    @classmethod
    def setUpTestData(cls):
        genre_1 = Genre.objects.create(name="Romance")
        genre_2 = Genre.objects.create(name="Thriller")
        genre_3 = Genre.objects.create(name="Drama")
        genre_4 = Genre.objects.create(name="Motivational")
        for i in range(1, 11):
            author = Author.objects.create(first_name=f"john_{i}", last_name=f"doe_{i}")
            book = Book.objects.create(title=f"book_{i}", author=author)
            book.genre.add(genre_1)
            book.genre.add(genre_2)
            book.genre.add(genre_3)
            book.genre.add(genre_4)

    def test_get_authors(self):
        response = self.client.get(f'/apps/library/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["author_list"])
        self.assertEqual(len(response.context["author_list"]), 10)

    def test_get_author(self):
        
        author = Author.objects.get(id=1)
        url = f'/apps/library/authors/{author.id}/'
        self.client.defaults['REMOTE_ADDR'] = LibraryViews.client_ip

        # Testing endpoint and response
        response = self.client.get(url)
        self.assertEqual(first=response.status_code, second=200, msg=f"the following url must be accessible: {url}")
        self.assertTrue(response.context["author"], msg="'author' key no present on View context")
        self.assertTrue(response.context["books"], msg="'books' key no present on View content")

        # Checking data consistency upon 1st day of visit...
        self.assertIn(member="device_id", container=response.client.cookies, msg="cookie 'device_id' MUST BE present")
        self.assertFalse(Visitor.objects.filter(device_id=response.client.cookies["device_id"].value),
                         msg="Visitor MUST NOT be registered on a 1st day of visit.")

        # Checking data consistency upon 2nd day of visit...
        response = self.client.get(url)
        visitor = Visitor.objects.filter(device_id=response.client.cookies["device_id"].value)
        self.assertTrue(visitor, msg="Visitor MUST BE registered on a 2nd day of visit.")
        self.assertEqual(visitor[0].device_id, response.client.cookies["device_id"].value,
                         msg="'device_id' MUST BE present on Visitor registry")
        self.assertEqual(visitor[0].ip_address, str(LibraryViews.client_ip),
                         msg="'ip_address' MUST BE present on Visitor registry")

        # Checking data consistency upon Visitor.days_visited field...
        self.client.get(url)
        visitor[0].refresh_from_db()
        self.assertEqual(first=visitor[0].days_visited, second=1,
                         msg="Visitor.days_visited MUST NOT be incremented with a visit on a same day.")

    def test_get_books(self):
        response = self.client.get(f'/apps/library/books/')

        # Check basic request response.
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["books"])

        # Check context query length with pagination applies.
        self.assertEqual(len(response.context["books"]), settings.PAGINATOR_PAGE_LENGTH)

        # Check page QS parameter.
        response = self.client.get('/apps/library/books/', {'page': '2'})
        self.assertEqual(response.status_code, 200)

        # Check page QS parameter with an invalid page number, for there are just 10 books...
        if settings.PAGINATOR_PAGE_LENGTH == 5:
            response = self.client.get('/apps/library/books/', {'page': '3'})
            self.assertEqual(response.status_code, 404)

        # Check book QS parameter (should return 2 books...)
        Book.objects.filter(id=1).update(title="Iron Arm")
        Book.objects.filter(id=2).update(title="The Great Mongol Army")
        response = self.client.get(f'/apps/library/books/', {'book': 'Arm'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["books"]), 2)

    def test_get_book(self):
        book = Book.objects.get(id=1)
        response = self.client.get(f'/apps/library/books/{book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.title, str(response.context["book"]))
