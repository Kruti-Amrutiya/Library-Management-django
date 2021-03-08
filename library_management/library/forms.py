from django import forms
from .models import User, Book, BookRecord, Student, Librarian


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'username', 'first_name', 'last_name', 'password', 'address', 'phone_num',  'profile_img', 'department']


class StudentAndFacultyUpdateForm(forms.Form):
    class Meta:
        model = User
        exclude = ('user', 'password')


class LibrarianUpdateForm(forms.Form):
    class Meta:
        model = Librarian
        fields = ['username', 'first_name', 'last_name', 'address', 'phone_num',  'profile_img']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
