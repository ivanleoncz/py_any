from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Book, Genre


class LibraryView(generic.View):

    template_name = "library/library.html"

    def get(self, request, *args, **kwargs):
        context = {
            'books': Book.objects.all().count(),
            'authors': Author.objects.all().count(),
            'genres': Genre.objects.all().count()
        }
        return render(request, self.template_name, context)


class AuthorListView(generic.ListView):

    template_name = "library/author.html"
    model = Author
    queryset = Author.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"author_list": self.queryset})


class AuthorDetailView(generic.View):

    template_name = "library/author_detail.html"

    def get(self, request, *args, **kwargs):
        author = get_object_or_404(Author, pk=self.kwargs["pk"])
        books = author.books.all()
        context = {
            "author": author,
            "books": books
        }
        return render(request, self.template_name, context)


class BookListView(generic.ListView):

    template_name = "library/book.html"
    model = Book

    def get_queryset(self):
        book = self.request.GET.get('book')
        if book:
            queryset = Book.objects.filter(title__icontains=book).order_by('title')
        else:
            queryset = Book.objects.order_by('title')
        return queryset

    def get(self, request, *args, **kwargs):
        page_number = self.request.GET.get('page')  # Provided by base template via page navigation.
        paginator = Paginator(self.get_queryset(), settings.PAGINATOR_PAGE_LENGTH)
        if page_number and int(page_number) > paginator.num_pages:
            return render(request, self.template_name, status=404)

        page = paginator.get_page(page_number)
        context = {
            'books': page.object_list,
            'page_obj': page,
            'is_paginated': True,
        }
        return render(request, self.template_name, context)


class BookDetailView(generic.DetailView):

    template_name = "library/book_detail.html"
    model = Book

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        return render(request, self.template_name, {"book": book})

