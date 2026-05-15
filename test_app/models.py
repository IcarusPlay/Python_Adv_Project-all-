import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# def get_disc_price_according_orig_price():
#     ...

def validate_phone_number(value: str) -> None:

    if not re.match(
            pattern=r"^\+?\d{1,4}?[\s-]?(?:\(?\d{2,5}\)?[\s-]?)?\d{2,5}[\s-]?\d{2,5}[\s-]?\d{0,5}$",
            string=value
    ):
        raise ValidationError(
            _("Invalid phone number. Please, try again.")
        )


gender_choices = [
    # ('то, что пойдёт в базу данных', 'то, что будет видеть клиент')
    ('m', 'Male'),
    ('f', 'Female'),
    ('na', 'N/A'),
]


roles = [
    ('admin', 'ADMIN'),
    ('moderator', 'MODERATOR'),
    ('lib-member', 'LIB_MEMBER'),
]



languages = [
    ('en', 'English'),
    ('ua', 'Ukrainian'),
    ('de', 'German'),
]

genres = [
    ('fiction', 'Fiction'),
    ('triller', 'Triller'),
]


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Username'),
        max_length=50,
        unique=True
    )
    email = models.EmailField(
        _('Email'),
        max_length=80,
        unique=True,
        null=True,
        blank=True
    )
    bio = models.TextField(
        _('Bio'),
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=50,
        null=True,
        blank=True
    )
    role = models.CharField(
        _('Role'),
        max_length=25,
        choices=roles,
        default='lib-member'
    )
    gender = models.CharField(
        _('Gender'),
        max_length=25,
        choices=gender_choices,
        default='na'
    )
    phone = models.CharField(
        _('Phone'),
        max_length=75,
        unique=True,
        null=True,
        blank=True,
        validators=[
            validate_phone_number,
        ]
    )
    birth_date = models.DateField(
        _("Birth Date"),
        null=True,
        blank=True
    )
    age = models.PositiveSmallIntegerField(
        _("Age"),
        null=True,
        blank=True,
        validators=[
            MinValueValidator(14),
            MaxValueValidator(120)
        ]
    )

    is_staff = models.BooleanField(
        _("Is Staff"),
        default=False
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
    )
    verified = models.BooleanField(
        _('Email'),
        default=False
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users"



class Book(models.Model):
    title = models.CharField(
        max_length=100,  # Обязятальный параметр для CharField, общий для строговых параметров, нужны миграции
        unique=True,  # общий для всех типов данных, нужны миграции
        verbose_name="Book name",  # общий для всех типов данных, НЕ нужны миграции
        help_text="You must provide specific name of book"  # общий для всех типов данных, НЕ нужны миграции
    )  # VarChar(255)
    description = models.TextField(
        null=True, # хранение null в БД общий для всех типов данных, нужны миграции
        blank=True # позволяет полю в Админ панели быть необязательным общий для всех типов данных, НЕ нужны миграции
    )
    language = models.CharField(
        max_length=30,
        choices=languages,
        null=True,
        blank=True
    )
    publisher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    genre = models.CharField(
        max_length=30,
        choices=genres,
        null=True,
        blank=True
    )
    price = models.FloatField()
    # discounted_price = models.FloatField()  # NOT NULL
    # discounted_price = models.FloatField(default=0.0)  # DEFAULT 0.0
    # discounted_price = models.FloatField(default=get_disc_price_according_orig_price)  # DEFAULT 0.0
    discounted_price = models.FloatField(null=True)  # NULLABLE
    published_date = models.DateField()

    # связи
    author = models.ForeignKey(
        'Author',
        # on_delete=models.DO_NOTHING,
        # on_delete=models.PROTECT,
        # on_delete=models.SET_DEFAULT, # (!!!!!!!!!! требует доп параметра default=)
        on_delete=models.SET_NULL, # (!!!!!!!!!! требует доп параметра null=True)
        null=True,
        # on_delete=models.SET(), # принимает как объект какую-то функцию, которая должна примениться к объектам
        # on_delete=models.CASCADE,

        related_name='books'
    )

    def __str__(self):
        return f"{self.title} {self.id}"

    class Meta:
        db_table = 'books'

        verbose_name = 'BOOK'
        verbose_name_plural = 'BOOKS'
        ordering = ['-published_date', 'title']

        get_latest_by = 'published_date'

        # unique_together = ('title', 'author')

        indexes = [
            models.Index(
                fields=['genre', 'language'],
                name='books_genre_language_idx'
            )
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='books_title_author_uqcst'
            )

        ]


# Миграции и управление моделями отвечают ИСКЛЮЧИТЕЛЬНО ЗА DDL категорию запросов

# DDL query -> Data Definition Language
# DML query -> Data Manipulation Language
# """
# CREATE TABLE IF NOT EXISTS 'test_app_book' (
#     id ...
#     title VarChar(100) NOT NULL
#     description TEXT NOT NULL
#     published_date DATE
# )
# """





class Author(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=35)
    pseudonym = models.CharField(max_length=20)
    bio = models.TextField(null=True)
    gender = models.CharField(
        max_length=4,
        choices=gender_choices,  # для строковых типов данных, необязательный нужны миграции
        default='na'  # общий для всех типов данных, нужны миграции
    )
    email = models.EmailField(max_length=75, null=True)
    # URLValidator() "под капотом" будет проверять, что строка начинается с http:// или https://
    website = models.URLField(null=True)

    # Integer fields
    age = models.PositiveSmallIntegerField(null=True)
    followers_count = models.PositiveIntegerField(null=True)
    posts_count = models.PositiveIntegerField(null=True)
    comments_count = models.PositiveIntegerField(null=True)
    reputation_score = models.DecimalField(
        null=True,
        max_digits=3,  # как много символов должно быть в общем. для Decimal типов, нужны миграции
        decimal_places=2  # из всего этого кол-ва как много должно быть после точки. для Decimal типов, нужны миграции
    )  #  1.00 | 3.75 | 5.00 | 4.99 | 2.01
    monetisation_income = models.FloatField(null=True)

    def __str__(self):
        # A. Sapkovsky
        return f"{self.first_name[0]}. {self.last_name}"

    class Meta:
        db_table = 'authors'


# monday = 14.99
# friday = 14.999999999999999999999999
# nickname = 'QnWr8AoKs' => 'qnwr8aoks'


# BigIntegerField             # [-15_000_000 | 15_000_000]
# IntegerField                # [-1_000_000 | 1_000_000]
# PositiveBigIntegerField     # [0 | 15_000_000]
# PositiveIntegerField        # [1_000_000]
# SmallIntegerField           # [-32_000 | 32_000]
# PositiveSmallIntegerField   # [0 | 32_000]
#
# FloatField                  # 1.1231231232 | 123123123.123232 | 7.313
# DecimalField                # 13.333 | 11.001 | 1.001



class Post(models.Model):
    title = models.CharField(
        max_length=200,
        unique_for_month='posted_at'  # Уникальный для Date колонок. передаём в виде строчки название Date колонки
    )  # важно, чтобы указаная колонка была НЕ auto_now(_add) и НЕ editable=False, иначе не сработает
    content = models.TextField()

    #  auto_now_add И auto_now параметры "под капотом" автоматичеки ставят ещё и параметр editable = False
    created_at = models.DateTimeField(auto_now_add=True)  # Срабатывает ОДИН раз ПРИ СОЗДАНИИ ОБЪЕКТА
    updated_at = models.DateTimeField(auto_now=True)  # Срабатывает ВСЕГДА. И при создании, И ПРИ ОБНОВЛЕНИИ
    reading_time = models.DurationField(
        null=True
    )
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'


# РАБОТА СО СВЯЗЯМИ
# models.OneToOneField  # o2o => один к одному
# models.ManyToManyField  # m2m => многие ко многим
# models.ForeignKey  # o2m => один ко многим
