from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Book, BookRecord, User, Student, Role
from library.forms import UserSignupForm, BookForm, StudentAndFacultyUpdateForm, LibrarianUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.forms.models import modelform_factory


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
            return HttpResponseRedirect('/login')
        else:
            messages.error(request, 'Username already exist!!')
            return HttpResponseRedirect('/signup')


class LoginView(View):
    def get(self, request):
        return render(request, 'library/login.html', {'form': AuthenticationForm()})

    def post(self, request):
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        user = auth.authenticate(request, username=uname, password=upass)
        if user is not None:
            auth.login(request, user)
            if user.role.role == 'Admin':
                return HttpResponseRedirect('/adminprofile')
            elif user.role.role == 'Student' or user.role.role == 'Faculty':
                return HttpResponseRedirect('/studentandfacultyprofile')
            else:
                return HttpResponseRedirect('/librarianprofile')
        else:
            messages.info(request, 'Invalid username or password', extra_tags='alert')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


class StudentProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'library/studentprofile.html')


class FacultyProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'library/facultyprofile.html')


class LibrarianProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'library/librarianprofile.html')


class AdminProfileView(LoginRequiredMixin, View):
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


class IssuebookView(View):
    def post(self, request, id):
        user = User.objects.get(username=request.user)
        count = Book.objects.all().count()
        print(count)
        bookrecords = BookRecord.objects.create(user=user, book=id)
        bookrecords.save()
        # avilable book and update in bookrecord update
        return render(request, 'library/issuebook.html', {'bookrecords': bookrecords})

    # def post(self, request):
    #     form = BookForm(request.POST)
    #     if form.is_valid():
    #         obj = Book()
    #         obj.title = request.POST.get('title')
    #         obj.author = request.POST.get('author')
    #         obj.save()
    #         return HttpResponseRedirect('/bookissued')


class StudentListView(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.get(role='Student')
        students = User.objects.filter(role=role)
        return render(request, 'library/studentlist.html', {'students': students})


class StudentDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            student = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/studentlist')
        return render(request, 'library/studentprofile.html', {'student': student})


class StudentUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            students = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/studentlist')
        form = StudentAndFacultyUpdateForm(instance=students)
        return render(request, "library/studentupdate.html", {'form': form})

    def post(self, request, id):
        students = User.objects.get(pk=id)
        form = StudentAndFacultyUpdateForm(request.POST, instance=students)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/studentlist')


class StudentDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            students = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/studentlist')
        students.delete()
        return HttpResponseRedirect('/studentlist')


class FacultyListView(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.get(role='Faculty')
        faculties = User.objects.filter(role=role)
        return render(request, 'library/facultylist.html', {'faculties': faculties})


class FacultyDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            faculty = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/facultylist')
        return render(request, 'library/facultyprofile.html', {'faculty': faculty})


class FacultyUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            faculties = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/facultylist')
        form = StudentAndFacultyUpdateForm(instance=faculties)
        return render(request, "library/facultyupdate.html", {'form': form})

    def post(self, request, id):
        faculties = User.objects.get(pk=id)
        form = StudentAndFacultyUpdateForm(request.POST, instance=faculties)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/facultylist')


class FacultyDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            faculties = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/facultylist')
        faculties.delete()
        return HttpResponseRedirect('/facultylist')


class LibrarianListView(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.get(role='Librarian')
        librarians = User.objects.filter(role=role)
        return render(request, 'library/librarianlist.html', {'librarians': librarians})


class LibrarianDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            librarian = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/librarianlist')
        return render(request, 'library/librarianprofile.html', {'librarian': librarian})


class LibrarianUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            librarians = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/librarianlist')
        form = LibrarianUpdateForm(instance=librarians)
        return render(request, "library/librarianupdate.html", {'form': form})

    def post(self, request, id):
        librarians = User.objects.get(pk=id)
        form = LibrarianUpdateForm(request.POST, instance=librarians)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/librarianlist')


class LibrarianDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            librarians = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/librarianlist')
        librarians.delete()
        return HttpResponseRedirect('/librarianlist')


# Book Listview
class BookListView(LoginRequiredMixin, ListView):
    template_name = "library/booklist.html"
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
            return HttpResponseRedirect('/booklist')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : '/booklist'}}">reload</a>""")


# Class to update any book data
class BookUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return HttpResponseRedirect('/booklist')
        form = BookForm(instance=book)
        return render(request, "library/bookadd.html", {'form': form})

    def post(self, request, id):
        book = Book.objects.get(pk=id)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/booklist')


# Class to delete any book from book list
class BookDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return HttpResponseRedirect('/booklist')
        book.delete()
        return HttpResponseRedirect('/booklist')
