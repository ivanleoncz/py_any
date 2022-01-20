from django.urls import path

from .views import LibraryView, AuthorListView, AuthorDetailView, BookListView, BookDetailView

urlpatterns = [
    path('library/', LibraryView.as_view(), name="library-view"),
    path('library/author/', AuthorListView.as_view(), name="author-view"),
    path('library/author/<int:pk>/', AuthorDetailView.as_view(), name="author-detail"),
    path('library/book/', BookListView.as_view(), name="book-view"),
    path('library/book/<int:pk>/', BookDetailView.as_view(), name="book-detail"),
]