from django.contrib import admin

from .models import Author, Book, Genre, BookInstance


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = (('first_name', 'last_name',),
              'date_of_birth', 'date_of_death')

    inlines = [BookInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    fields = ('title', 'author', 'isbn_10', 'isbn_13', 'genre', 'summary')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
