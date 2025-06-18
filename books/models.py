from __future__ import unicode_literals

from django.db import models



class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    published_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
