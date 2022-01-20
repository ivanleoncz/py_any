from django.shortcuts import render
from django.views import generic

from .models import Author, Book


class LibraryView(generic.TemplateView):

    template_name = "library/library.html"


class AuthorListView(generic.ListView):

    model = Author
    template_name = "library/author.html"
    queryset = Author.objects.all().order_by('id')


class AuthorDetailView(generic.DetailView):

    model = Author
    template_name = "library/author_detail.html"


class BookListView(generic.ListView):

    model = Book
    template_name = "library/book.html"
    queryset = Book.objects.all().order_by('id')


class BookDetailView(generic.DetailView):

    model = Book
    template_name = "library/book_detail.html"

