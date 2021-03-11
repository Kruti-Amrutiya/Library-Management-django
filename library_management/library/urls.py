from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view.as_view(), name='home'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('validate_username/', views.ValidateUsername.as_view(), name='validate_username'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('studentprofile', views.StudentProfileView.as_view(), name='studentprofile'),
    path('facultyprofile', views.FacultyProfileView.as_view(), name='facultyprofile'),
    path('librarianprofile', views.LibrarianProfileView.as_view(), name='librarianprofile'),
    path('adminprofile', views.AdminProfileView.as_view(), name='adminprofile'),

    path('studentlist/', views.StudentListView.as_view(), name='studentlist'),
    path('studentdetail/<int:id>/', views.StudentDetailView.as_view(), name='studentdetail'),
    path('studentdelete/<int:id>/', views.StudentDeleteView.as_view(), name='studentdelete'),

    path('facultylist/', views.FacultyListView.as_view(), name='facultylist'),
    path('facultydetail/<int:id>/', views.FacultyDetailView.as_view(), name='facultydetail'),
    path('facultydelete/<int:id>/', views.FacultyDeleteView.as_view(), name='facultydelete'),

    path('librarianlist/', views.LibrarianListView.as_view(), name='librarianlist'),
    path('librariandetail/<int:id>/', views.LibrarianDetailView.as_view(), name='librariandetail'),
    path('librariandelete/<int:id>/', views.LibrarianDeleteView.as_view(), name='librariandelete'),

    path('copies_of_books/', views.CopiesOfBooks.as_view(), name='copies_of_books'),
    path('booklist', views.BookListView.as_view(), name='booklist'),
    path('bookdetail/<int:id>', views.BookDetailView.as_view(), name='bookdetail'),
    path('bookadd/', views.BookAddView.as_view(), name='bookadd'),
    path('bookupdate/<int:id>', views.BookUpdateView.as_view(), name='bookupdate'),
    path('bookdelete/<int:id>', views.BookDeleteView.as_view(), name='bookdelete'),

    path('viewissuedbookbystudent/', views.ViewIssuedBooksByStudent.as_view(), name='viewissuedbookbystudent'),
    path('viewissuedbooks/', views.ViewIssuedBooks.as_view(), name='viewissuedbooks'),
    path('bookissue/<int:id>/', views.IssueBookView.as_view(), name='bookissue'),
    # path('viewissuedbooksrequest/', views.ViewIssuedBooksRequest.as_view(), name='viewissuedbooksrequest'),
]
