from django.shortcuts import render
from django.views import generic

from .models import Author


class LibraryView(generic.View):

    template = 'library.html'

    def get(self, request):
        return render(request, self.template)


class AuthorListView(generic.ListView):

    model = Author
    template_name = "author.html"
    queryset = Author.objects.all()


class AuthorDetailView(generic.DetailView):

    model = Author
    template_name = "author_detail.html"

