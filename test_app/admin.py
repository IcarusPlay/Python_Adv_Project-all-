from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.functions import Round
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import F

from test_app.models import Book, Author, Post, User



# # class BasicInlineForm(admin.TabularInline):
# class BasicInlineForm(admin.StackedInline):
#
#     model = MyModel  # привязка к модели
#     extra = 1  # кол-во форм, которое будет отображаться по умолчанию для новых записей
#     min_num = 1  # минимальное кол-во форм
#     max_num = 10  # максимальное кол-во форм
#
#     fields = ['field_1', 'field_2', ..., 'field_100500']  # какие поля будут для отображения
#     fieldsets = (
#         ('Group Name', {'fields': ['field_1', 'field_2', ..., 'field_100500']}),
#     )
#     readonly_fields = ['field_1', 'field_2', ..., 'field_100500']  # список полей только на отображение
#     can_delete = True  # разрешить удаление записей, или нет
#     show_change_link = True  # разрашить \ запретить отображение ссылки на редактирование (иконка карандашика)
#     ordering = ['-field'] # сортировка объектов



# class BookInline(admin.StackedInline):
class BookInline(admin.TabularInline):
    model = Book

    extra = 1
    max_num = 3


# class AuthorInline(admin.StackedInline):
#     model = Author
#
#     extra = 1
#     max_num = 5


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline
    ]

    list_display = [
        'first_name',
        'last_name',
        'gender',
        'reputation_score',
    ]
    search_fields = [
        'last_name',
        'pseudonym',
    ]
    list_filter = [
        'gender'
    ]


class CustomUserAdmin(BaseUserAdmin):

    # специальный параметр, который моможет нам разбить
    # все наши поля на логические группки
    # fieldsets -- это настройка для обновления объектов
    #
    # Вся эта настройка идёт как кортеж с кортежами
    #
    # Каждый кортеж -- одна логическая группка
    # Внутри кортежа два главных параметра:
    #     название группы (или None, или строчка)
    #     и словарь с настройками. Мы берём пока что только настройку fields
    #     в которой последним кортежем (да, их много, понимаю) мы уже передаём
    #     какие колонки мы хотим видеть в этой группе
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('birth_date',)}),
    )

    # а вот эта вот настройка поможет нам разбить поля на логические
    # группки при создании объекта
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
    # inlines = [AuthorInline]

    list_display = [
        'title',
        'show_description',
        'language',
        'genre',
        'visual_price',
        'discounted_price',
        'published_date',
        'author',
        # 'new_field',
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

    actions = [
        'increase_price_by_ten_percent'
    ]


    # !!!!!!!!!!!!!!!!!!!!!!!! CUSTOM FIELDS !!!!!!!!!!!!!!!!!!!!!!!!!!
    @admin.display(description="About")
    def show_description(self, obj: Book) -> str:
        if not obj.description:
            return "No Description"
        else:
            if len(obj.description) < 15:
                return obj.description
            return f"{obj.description[:30]}..."


    @admin.display(description='TEST')
    def new_field(self, obj):
        return "GREETINGS"


    @admin.display(description="Price")
    def visual_price(self, obj: Book):
        if obj.price < 10:
            color = "green"
        elif 10 <= obj.price < 20:
            color = "orange"
        else:
            color = "red"

        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.price
        )


    # !!!!!!!!!!!!!!!!!!!! CUSTOM ACTIONS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    @admin.action(description="Увеличить цену на 10 %%")
    def increase_price_by_ten_percent(self, request, objects):
        objects.update(
            price=Round(
                F('price') * 1.1,
                precision=2
            )
        )


# admin.site.register(Book, BookAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group)
# admin.site.register(Author)
admin.site.register(Post)