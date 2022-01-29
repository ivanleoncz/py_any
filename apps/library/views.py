from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Book, Genre


class LibraryView(generic.TemplateView):

    template_name = "library/library.html"
    extra_context = {
        'books': Book.objects.all().count(),
        'authors': Author.objects.all().count(),
        'genres': Genre.objects.all().count()
    }


class AuthorListView(generic.ListView):

    model = Author
    template_name = "library/author.html"
    queryset = Author.objects.all().order_by('id')


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


class BookDetailView(generic.DetailView):

    model = Book
    template_name = "library/book_detail.html"

