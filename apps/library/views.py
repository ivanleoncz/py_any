from django.shortcuts import render
from django.views import generic

from .models import Author


class LibraryView(generic.TemplateView):

    template_name = "library/library.html"


class AuthorListView(generic.ListView):

    model = Author
    template_name = "library/author.html"
    queryset = Author.objects.all()


class AuthorDetailView(generic.DetailView):

    model = Author
    template_name = "library/author_detail.html"

