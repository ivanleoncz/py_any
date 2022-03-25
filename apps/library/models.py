import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from PIL import Image


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='library/authors/', null=True, blank=True,
                                help_text='will be automatically convert the image to 256x256',
                                validators=[FileExtensionValidator(['jpeg', 'jpg', 'png'])])
    about = models.TextField(max_length=1024, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        verbose_name = "Authors"
        verbose_name_plural = "Authors"
        ordering = ['last_name', 'first_name']
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_of_death__gt=models.F('date_of_birth')),
                name='check_date_of_death',
            ),
        ]

    def get_absolute_url(self):
        return reverse('authors-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def save(self, *args, **kwargs):
        if self.picture:
            output_size = 256, 256
            super().save(*args, **kwargs)
            img = Image.open(self.picture.path)
            img.thumbnail(output_size)
            img.save(self.picture.path)
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=32, help_text='Enter a book genre (e.g. Romance)')

    class Meta:
        verbose_name = "Genres"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey('Author', related_name="books", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=512, help_text='Enter a brief description')
    isbn_10 = models.CharField(null=True, blank=True, max_length=13, unique=True,
                               help_text='<a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>')
    isbn_13 = models.CharField(null=True, blank=True, max_length=13, unique=True,
                               help_text='<a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>')
    genre = models.ManyToManyField(Genre, related_name="books", help_text='Select a genre for this book')

    class Meta:
        verbose_name = "Books"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])


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