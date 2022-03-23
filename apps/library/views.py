from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Book, Genre
from apps.geotracking.utils import Utils


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
            qs = self.get_queryset().filter(title__icontains=book)
        else:
            qs = self.get_queryset().order_by('title')
        # Paginator object
        paginator = Paginator(qs, 5)
        page_number = self.request.GET.get('page')
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

