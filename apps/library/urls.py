from django.urls import path

from .views import LibraryView, AuthorListView, AuthorDetailView, BookListView, BookDetailView

urlpatterns = [
    path('library/', LibraryView.as_view(), name="library-view"),
    path('library/authors/', AuthorListView.as_view(), name="authors-view"),
    path('library/authors/<int:pk>/', AuthorDetailView.as_view(), name="authors-detail"),
    path('library/books/', BookListView.as_view(), name="books-view"),
    path('library/books/<int:pk>/', BookDetailView.as_view(), name="books-detail"),
]