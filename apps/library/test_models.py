from django.test import TestCase

from .models import Author, Book, Genre


class MyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author_first_name = "John"
        cls.author_last_name = "Doe"
        cls.author = Author.objects.create(first_name=cls.author_first_name,
                                           last_name=cls.author_last_name)
        cls.genre_1 = Genre.objects.create(name="Romance")
        cls.genre_2 = Genre.objects.create(name="Drama")
        cls.genre_3 = Genre.objects.create(name="Adventure")
        cls.genre_4 = Genre.objects.create(name="Thriller")
        cls.book = Book.objects.create(title="John's Book", author=cls.author)
        cls.book.genre.add(cls.genre_1)
        cls.book.genre.add(cls.genre_2)
        cls.book.genre.add(cls.genre_3)
        cls.book.genre.add(cls.genre_4)

    def test_author_creation(self):
        self.assertTrue(self.author)

    def test_author_object_name(self):
        expected_author_name = ", ".join((self.author.last_name, self.author.first_name))
        self.assertEqual(str(self.author), expected_author_name)

    def test_author_date_of_death_label(self):
        self.assertEqual(self.author._meta.get_field('date_of_death').verbose_name, "Died")

    def test_author_reverse_url(self):
        self.assertEqual(self.author.get_absolute_url(), f'/apps/library/authors/{self.author.id}/')

    def test_book_creation(self):
        self.assertTrue(self.book)

    def test_book_reverse_url(self):
        self.assertEqual(self.book.get_absolute_url(), f'/apps/library/books/{self.book.id}/')

    def test_book_display_genre(self):
        # Even though a book can have multiple genres (and vice versa),
        # Genre model should display only the first 3 genres...
        self.assertEqual(len(self.book.display_genre().split(',')), 3)

    def test_book_existence_after_author_deletion(self):
        self.author.delete()
        self.author = Author.objects.filter(first_name=self.author_first_name,
                                            last_name=self.author_last_name)
        self.assertFalse(self.author)
        self.assertTrue(self.book)

