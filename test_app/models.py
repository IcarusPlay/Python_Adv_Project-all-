from django.db import models

# Create your models here.

# def get_disc_price_according_orig_price():
#     ...


class Book(models.Model):
    title = models.CharField(max_length=100)  # VarChar(255)
    description = models.TextField()
    price = models.FloatField()
    # discounted_price = models.FloatField()  # NOT NULL
    # discounted_price = models.FloatField(default=0.0)  # DEFAULT 0.0
    # discounted_price = models.FloatField(default=get_disc_price_according_orig_price)  # DEFAULT 0.0
    discounted_price = models.FloatField(null=True)  # NULLABLE
    published_date = models.DateField()
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
