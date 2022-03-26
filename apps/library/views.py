from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Book, Genre
from apps.geotracking.utils import Utils
from py_any.settings import PAGINATOR_PAGE_LENGTH


class LibraryView(generic.View, Utils):

    template_name = "library/library.html"

    def get(self, request, *args, **kwargs):
        context = {
            'books': Book.objects.all().count(),
            'authors': Author.objects.all().count(),
            'genres': Genre.objects.all().count()
        }
        self.store_ip_data(request)
        return render(request, self.template_name, context)


class AuthorListView(generic.ListView, Utils):

    model = Author
    template_name = "library/author.html"
    queryset = Author.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        self.store_ip_data(request)
        return render(request, self.template_name, {"author_list": self.queryset})


class AuthorDetailView(generic.View, Utils):

    template_name = "library/author_detail.html"

    def get(self, request, *args, **kwargs):
        self.store_ip_data(request)
        author = get_object_or_404(Author, pk=self.kwargs["pk"])
        books = author.books.all()
        context = {
            "author": author,
            "books": books
        }
        return render(request, self.template_name, context)


class BookListView(generic.ListView, Utils):

    model = Book
    template_name = "library/book.html"

    def get(self, request, *args, **kwargs):
        self.store_ip_data(request)
        book = self.request.GET.get('book')
        if book:
            qs = self.get_queryset().filter(title__icontains=book).order_by('title')
        else:
            qs = self.get_queryset().order_by('title')
        # Paginator object
        paginator = Paginator(qs, PAGINATOR_PAGE_LENGTH)
        page_number = self.request.GET.get('page')
        if page_number and int(page_number) > paginator.num_pages:
            return render(request, self.template_name, status=404)
        page_obj = paginator.get_page(page_number)
        context = {
            'book_list': page_obj,  # paginator
            'page_obj': page_obj,  #
            'is_paginated': True,
        }
        return render(request, self.template_name, context)


class BookDetailView(generic.DetailView, Utils):

    model = Book
    template_name = "library/book_detail.html"

    def get(self, request, *args, **kwargs):
        self.store_ip_data(request)
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        return render(request, self.template_name, {"book": book})

