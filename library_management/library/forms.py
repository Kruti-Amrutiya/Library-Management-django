from django import forms
from .models import User, Book, BookRecord


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'username', 'first_name', 'last_name', 'password', 'address', 'phone_num',  'profile_img', 'department']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
