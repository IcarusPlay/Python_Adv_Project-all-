from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100) #VarChar (255(numbers) SQL
    description =models.TextField()
    price = models.FloatField()
    published_date =models.DateField()


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
