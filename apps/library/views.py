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
    paginate_by = 5
    template_name = "library/book.html"

    def get_queryset(self):
        book = self.request.GET.get('book')
        if book:
            book_list = Book.objects.all().filter(title__icontains=book)
        else:
            book_list = Book.objects.all().order_by('id')
        return book_list

    def get(self, request, *args, **kwargs):
        self.store_ip_data(request)
        return render(request, self.template_name, {"book_list": self.get_queryset()})


class BookDetailView(generic.DetailView, Utils):

    model = Book
    template_name = "library/book_detail.html"

    def get(self, request, *args, **kwargs):
        self.store_ip_data(request)
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        return render(request, self.template_name, {"book": book})

