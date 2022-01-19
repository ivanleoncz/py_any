from django.urls import path

from .views import LibraryView, AuthorListView, AuthorDetailView

urlpatterns = [
    path('library/', LibraryView.as_view(), name="library"),
    path('library/author/', AuthorListView.as_view(), name="author_all"),
    path('library/author/<int:pk>/', AuthorDetailView.as_view(), name="author")
]