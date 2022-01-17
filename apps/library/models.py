import uuid

from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        verbose_name = "Authors"
        verbose_name_plural = "Authors"
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Genre(models.Model):
    name = models.CharField(max_length=32, help_text='Enter a book genre (e.g. Romance)')

    class Meta:
        verbose_name = "Genres"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=512, help_text='Enter a brief description')
    isbn = models.CharField(max_length=13, unique=True,
                            help_text='<a href="https://www.isbn-international.org/content/what-isbn">What is ?</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    class Meta:
        verbose_name = "Books"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    STATUS = ((0, 'Available'), (1, 'On loan'), (2, 'Reserved'), (3, 'Maintenance'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for the book across whole library')
    book = models.ForeignKey('Book', on_delete=models.PROTECT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True, help_text='Date when the book should be returned')
    status = models.PositiveIntegerField(choices=STATUS, blank=True, default=0, help_text='Book availability')

    class Meta:
        verbose_name = "Instances"
        verbose_name_plural = "Instances"
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title}) - {dict(self.STATUS)[self.status]}'