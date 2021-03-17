from django.contrib import admin
from .models import User, Student, Faculty, Librarian, Book, BookRecord, Role, Department, Category

admin.site.site_header = 'Library admin'

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Librarian)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Category)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('role', 'username', 'first_name', 'last_name', 'email', 'password', 'address', 'phone_num', 'profile_img', 'department')
    ordering = ('username',)
    search_fields = ("username",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'book_img', 'total_copies_of_books', 'available_copies_of_books')
    ordering = ('title',)
    search_fields = ("title", "author", "category")


@admin.register(BookRecord)
class BookRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'issue_date', 'due_date', 'return_date')
    ordering = ('issue_date',)
    search_fields = ("book",)
