from django import forms
from .models import User, Book
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['role', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'address', 'phone_num',  'profile_img', 'department']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
