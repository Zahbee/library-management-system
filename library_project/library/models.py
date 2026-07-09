from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


# class Borrow(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     due_date = models.DateTimeField(null=True, blank=True)
#     return_date = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=20, default="Borrowed")

#     def __str__(self):
#         return f"{self.user.username} - {self.book.title}"

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="Borrowed")

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

