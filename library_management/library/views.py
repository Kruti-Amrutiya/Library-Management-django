from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Book, BookRecord, User
from library.forms import UserSignupForm, BookForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import modelform_factory


# HOME PAGE
class home_view(View):
    def get(self, request):
        return render(request, 'library/index.html')


class UserSignupView(View):
    def get(self, request):
        return render(request, 'library/signup.html', {'form': UserSignupForm()})

    def post(self, request):
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password']
            form1 = form.save(commit=False)
            form1.set_password(password)
            form1.save()
            print(form1.role)
            if (str(form1.role) == 'Admin'):
                return HttpResponseRedirect('/adminprofile')
            else:
                return HttpResponseRedirect('/studentprofile')
        else:
            messages.error(request, 'Username already exist!!')
            return HttpResponseRedirect('/signup')
        return HttpResponseRedirect('/login')


class LoginView(View):
    def get(self, request):
        return render(request, 'library/login.html', {'form': AuthenticationForm()})

    def post(self, request):
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        user = auth.authenticate(request, username=uname, password=upass)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect('/adminprofile')
            else:
                return HttpResponseRedirect('/studentprofile')
        else:
            messages.info(request, 'Invalid username or password', extra_tags='alert')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


class StudentProfileView(View):
    def get(self, request):
        return render(request, 'library/studentprofile.html')


class LibrarianProfileView(View):
    def get(self, request):
        return render(request, 'library/librarianprofile.html')


class AdminProfileView(View):
    def get(self, request):
        return render(request, 'library/adminprofile.html')


# View will return bookrecords
class ViewIssuedBooksByStudent(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        bookrecords = BookRecord.objects.filter(user=user)
        return render(request, 'library/viewissuedbookbystudent.html', {'bookrecords': bookrecords})


class ViewIssuedBooks(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        bookrecords = BookRecord.objects.filter(user=user)
        return render(request, 'library/viewissuedbooks.html', {'bookrecords': bookrecords})


class BookIndexView(LoginRequiredMixin, ListView):
    template_name = "library/bookindex.html"
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()


# Class to add any book data
class BookAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = BookForm()
        return render(request, 'library/bookadd.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bookindex')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : '/bookindex'}}">reload</a>""")


# Class to update any book data
class BookUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return HttpResponseRedirect('/bookindex')
        form = BookForm(instance=book)
        return render(request, "library/bookadd.html", {'form': form})

    def post(self, request, id):
        book = Book.objects.get(pk=id)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/bookindex')


# Class to delete any book from book list
class BookDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return HttpResponseRedirect('/bookindex')
        book.delete()
        return HttpResponseRedirect('/bookindex')
