from django.contrib import admin

from test_app.models import Book, Author, Post

admin.site.register(Author)
admin.site.register(Post)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'language',
        'genre',
        'price',
        'discounted_price',
        'published_date',
        'author',
    ]

    search_fields = [
        'title',
        'description',
        'author__last_name',
    ]

    list_filter = [
        'language',
        'genre',
    ]

    list_editable = [
        'language',
        'genre',
    ]



#admin.site.register(Book, BookAdmin)