from django import forms
from .models import User, Book
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core import validators


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['role', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'phone_num',  'profile_img', 'department']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
            print(match)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address already exists!!!')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
