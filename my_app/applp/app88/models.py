from django.db import models

# Create your models here.
class Publisher(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=32, unique=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=32, unique=True)
    books = models.ManyToManyField('Book')

    def __str__(self):
        return self.name


class Author_book(models.Model):
    author = models.ForeignKey('Author')
    book = models.ForeignKey('Book')
    date = models.DateTimeField()

