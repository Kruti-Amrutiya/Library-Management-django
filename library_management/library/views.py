from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Book, BookRecord, User, Role
from library.forms import UserSignupForm, BookForm, BookUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from library_management.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.http import JsonResponse


# Home Page
class home_view(View):
    def get(self, request):
        return render(request, 'library/index.html')


# User SignupForm
class UserSignupView(View):
    def get(self, request):
        return render(request, 'library/signup.html', {'form': UserSignupForm()})

    def post(self, request):
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            subject = 'Welcome to Library Management System'
            message = 'Hope you are enjoying your Django Project'
            recepient = str(form['email'].value())
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            form1 = form.save(commit=False)
            form1.save()
            return HttpResponseRedirect('/login')
        else:
            print(form.errors)
            messages.error(request, 'Username already exist!!')
            return HttpResponseRedirect('/signup')


# Username validation
class ValidateUsername(View):
    def get(self, request):
        username = request.GET.get('username', None)
        data = {
            'is_taken': User.objects.filter(username=username).exists()
        }
        return JsonResponse(data)


# User LoginForm
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
            elif user.role.role == 'Student':
                return HttpResponseRedirect('/studentprofile')
            elif user.role.role == 'Faculty':
                return HttpResponseRedirect('/facultyprofile')
            else:
                return HttpResponseRedirect('/librarianprofile')
        else:
            messages.info(request, 'Invalid username or password', extra_tags='alert')


# User LogOut
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


class IssueBookView(View):
    def post(self, request, id):
        user = User.objects.get(username=request.user)
        book_count = Book.objects.all().count()
        print(book_count)
        bookrecords = BookRecord.objects.create(user=user, book=id)
        bookrecords.save()
        # avilable book and update in bookrecord update
        return render(request, 'library/issuebook.html', {'bookrecords': bookrecords})


# Student List View in admin dashboard
class StudentListView(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.get(role='Student')
        students = User.objects.filter(role=role)
        return render(request, 'library/studentlist.html', {'students': students})


# Student Details View in admin dashboard
class StudentDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            student = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/studentlist')
        return render(request, 'library/studentdetail.html', {'student': student})


# Student delete View in admin dashboard
class StudentDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            students = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/studentlist')
        students.delete()
        return HttpResponseRedirect('/studentlist')


# Faculty list View in admin dashboard
class FacultyListView(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.get(role='Faculty')
        faculties = User.objects.filter(role=role)
        return render(request, 'library/facultylist.html', {'faculties': faculties})


# Faculty details View in admin dashboard
class FacultyDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            faculty = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/facultylist')
        return render(request, 'library/facultydetail.html', {'faculty': faculty})


# Faculty delete View in admin dashboard
class FacultyDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            faculties = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/facultylist')
        faculties.delete()
        return HttpResponseRedirect('/facultylist')


# Librarian list View in admin dashboard
class LibrarianListView(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.get(role='Librarian')
        librarians = User.objects.filter(role=role)
        return render(request, 'library/librarianlist.html', {'librarians': librarians})


# Librarian details View in admin dashboard
class LibrarianDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            librarian = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponseRedirect('/librarianlist')
        return render(request, 'library/librariandetail.html', {'librarian': librarian})


# Librarian delete View in admin dashboard
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


# Book Details
class BookDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return HttpResponseRedirect('/booklist')
        return render(request, 'library/bookdetail.html', {'book': book})


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
        form = BookUpdateForm(instance=book)
        return render(request, "library/bookupdate.html", {'form': form, 'book': book})

    def post(self, request, id):
        book = Book.objects.get(pk=id)
        form = BookUpdateForm(request.POST, instance=book)
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


class CopiesOfBooks(View):
    def post(self, request):
        id = request.POST.get('book_id')
        book = Book.objects.get(id=id)
        success = True
        if request.POST['action'] == 'increment':
            book.total_copies_of_books += 1
            book.available_copies_of_books += 1
        else:
            if book.available_copies_of_books < 1:
                if book.total_copies_of_books < 2:
                    success = False
                else:
                    book.total_copies_of_books -= 1
            else:
                book.total_copies_of_books -= 1
                book.available_copies_of_books -= 1
       
        book.save()
        return JsonResponse({'copies_of_books': book.total_copies_of_books, 'available_copies': book.available_copies_of_books, 'success': success})
