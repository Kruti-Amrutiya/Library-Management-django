from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from library.models import Book, BookRecord, User, Role, Student, Faculty, Librarian, Admin
from library.forms import UserSignupForm, BookForm, BookUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages, auth
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from library_management.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Q
import datetime


# Home Page
class home_view(View):
    def get(self, request):
        # to understand the concept of managers
        # return render(request, 'library/index.html', {'user': User.users.get_stu_id_range(3, 6)})
        return render(request, 'library/index.html')


# User SignupForm
class UserSignupView(View):
    def get(self, request):
        return render(request, 'library/signup.html', {'form': UserSignupForm()})

    def post(self, request):
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            # subject = 'Welcome to Library Management System'
            # message = 'Thank you for registration in Library Management System!!!'
            # recepient = str(form['email'].value())
            # send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            user = form.save()

            if form.cleaned_data['role'].role == 'Admin':
                Admin.objects.create(user=user)
            elif form.cleaned_data['role'].role == 'Student':
                Student.objects.create(user=user)
            elif form.cleaned_data['role'].role == 'Faculty':
                Faculty.objects.create(user=user)
            elif form.cleaned_data['role'].role == 'Librarian':
                Librarian.objects.create(user=user)
            else:
                return render(request, 'library/userprofile.html', {'user': user})

            # user login
            login(request, user)

            # login for specific user
            if Role == 'Admin':
                return HttpResponseRedirect('/adminprofile')
            else:
                return render(request, 'library/userprofile.html', {'user': user})
        else:
            print(form.errors)
            return render(request, 'library/signup.html', {'form': UserSignupForm()})


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
            else:
                return render(request, 'library/userprofile.html', {'user': user})
        else:
            messages.info(request, 'Invalid username or password', extra_tags='alert')
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))


# User LogOut
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


# User Profile View
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        return render(request, 'library/userprofile.html', {"user": user})


# Admin Profile View
class AdminProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'library/adminprofile.html')


# View will return bookrecords
class ViewTotalIssuedBooks(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        book_records = BookRecord.objects.filter(user=user)
        return render(request, 'library/issuedbooks.html', {'book_records': book_records})


# Class for issue book from library
class BookIssueView(LoginRequiredMixin, View):
    def post(self, request, id):
        flag = 0
        books = Book.objects.get(id=id)
        all_book_records = BookRecord.objects.filter(book__title__iexact=books.title)
        for current_user in all_book_records:
            if current_user.user == request.user and current_user.return_date is None:
                flag = 1
                messages.error(request, "Book Already Issued")
                return HttpResponseRedirect('/booklist')

        if flag == 0:
            all_user_records = BookRecord.objects.filter(Q(user__username__iexact=str(request.user)) & Q(return_date=None)).count()
            if all_user_records > 2:
                messages.error(request, "You cannot issue more than 3 books")
                return HttpResponseRedirect('/booklist')
            elif books.available_copies_of_books == 0:
                messages.error(request, 'This book is out of stock!!')
                return HttpResponseRedirect('/booklist')
            elif books.available_copies_of_books > 0:
                books.available_copies_of_books -= 1
                books.save()
                issue_book_record = BookRecord.objects.create(user=request.user, book=books)
                issue_book_record.save()
                messages.info(request, 'Book issue successfully!!')
            return HttpResponseRedirect('/viewtotalissuedbooks')


# Class for return book to library
class BookReturnView(LoginRequiredMixin, View):
    def post(self, request, id):
        present_book = BookRecord.objects.get(id=id)
        if present_book:
            present_book.return_date = datetime.datetime.now()
            present_book.save()
            books = Book.objects.get(title=present_book.book.title)
            books.available_copies_of_books += 1
            books.save()
            messages.info(request, 'Book return successfully!!')
        else:
            messages.error(request, 'There is no books available!!')
        return HttpResponseRedirect('/booklist')


# Title search
class SearchBox(LoginRequiredMixin, View):
    def post(self, request):
        search_str = request.POST.get('searchText')
        books = Book.objects.filter(title__icontains=search_str)
        context = []
        for book in books:
            details = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'category': book.category.category,
                'book_img': book.book_img.url,
                'total_copies_of_books': book.total_copies_of_books,
                'available_copies_of_books': book.available_copies_of_books
            }
            context.append(details)
        return JsonResponse(context, safe=False)


# Autocomplete view for search any book
class AutoCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        if 'term' in request.GET:
            book_records = BookRecord.objects.filter(book__title__icontains=request.GET.get('term'))
            titles = list()

            for books in book_records:
                titles.append(books.book.title) 
            return JsonResponse(titles, safe=False)


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


# User delete View in admin dashboard
class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        user = User.objects.get(id=id)
        new_role = user.role.role
        user.delete()

        if new_role == 'Student':
            return HttpResponseRedirect('/studentlist')
        elif new_role == 'Faculty':
            return HttpResponseRedirect('/facultylist')
        else:
            return HttpResponseRedirect('/librarianlist')


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


# Book Listview
class BookListView(LoginRequiredMixin, ListView):
    template_name = "library/booklist.html"
    model = Book
    context_object_name = 'books'
    paginate_by = 3


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


# Copies of books
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
