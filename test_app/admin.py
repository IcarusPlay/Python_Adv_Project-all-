from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from test_app.models import Book, Author, Post, User


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'birth_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('gender', 'role')
    ordering = ('username',)


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
        'genre'
    ]

    list_editable = [
        'language',
        'genre'
    ]


# admin.site.register(Book, BookAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Author)
admin.site.register(Post)
