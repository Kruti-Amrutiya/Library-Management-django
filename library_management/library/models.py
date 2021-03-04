from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import datetime


# Create your models here.
class Role(models.Model):
    TYPE = (
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('Librarian', 'Librarian'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=255, choices=TYPE, null=True, blank=True)

    def __str__(self):
        return self.role


class Department(models.Model):
    DEPART = (
        ('Computer', 'Computer Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Civil', 'Civil Engineering'),
        ('Electronics & Communication', 'Electronics Engineering'),
        ('Electrical', 'Electrical Engineering'),
        ('Mechanical', 'Mechanical Engineering'),
    )
    department = models.CharField(max_length=255, choices=DEPART, null=True, blank=True)

    def __str__(self):
        return self.department


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    phone_num = PhoneNumberField(null=True, blank=True, unique=True)
    profile_img = models.ImageField(blank=True, upload_to='profile_image/', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    CAT = (
        ('History', 'History'),
        ('Technical', 'Technical'),
        ('Educational', 'Educational'),
        ('Biography', 'Biography'),
        ('Cooking', 'Cooking'),
        ('Comics', 'Comics'),
        ('Health', 'Health'),
        ('Travel', 'Travel'),
        ('Horror', 'Horror'),
        ('Mystery', 'Mystery'),
        ('Art & Craft', 'Art & Craft'),
        ('Sports', 'Sports'),
        ('Religion', 'Religion'),
        ('Kids', 'Kids'),
        ('Business', 'Business'),
    )
    category = models.CharField(max_length=255, choices=CAT, blank=True, null= True)

    def __str__(self):
        return self.category


class Book(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Select a category for this book", null=True, blank=True)
    book_img = models.ImageField(blank=True, null=True, upload_to='book_image/')
    total_copies_of_books = models.BigIntegerField(default=None, null=True, blank=True)
    available_copies_of_books = models.BigIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.title


class BookRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    due_date = models.DateTimeField(default=None, null=True, blank=True, editable=False)
    return_date = models.DateTimeField(default=None, null=True, blank=True)

    def Book_due_date(self):
        self.due_date = self.issue_date + datetime.timedelta(days=10)

    def save(self, *args, **kwargs):
        from datetime import datetime, timedelta
        self.due_date = datetime.now() + timedelta(days=10)
        super(BookRecord, self).save(*args, **kwargs)

    def __str__(self):
        return self.book.title
