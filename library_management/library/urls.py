from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home_view.as_view(), name='home'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('validate_username/', views.ValidateUsername.as_view(), name='validate_username'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('userprofile/<int:id>/', views.UserProfileView.as_view(), name='userprofile'),
    path('adminprofile', views.AdminProfileView.as_view(), name='adminprofile'),

    path('studentlist/', views.StudentListView.as_view(), name='studentlist'),
    path('studentdetail/<int:id>/', views.StudentDetailView.as_view(), name='studentdetail'),
    path('userdelete/<int:id>/', views.UserDeleteView.as_view(), name='userdelete'),

    path('facultylist/', views.FacultyListView.as_view(), name='facultylist'),
    path('facultydetail/<int:id>/', views.FacultyDetailView.as_view(), name='facultydetail'),

    path('librarianlist/', views.LibrarianListView.as_view(), name='librarianlist'),
    path('librariandetail/<int:id>/', views.LibrarianDetailView.as_view(), name='librariandetail'),

    path('autocompletesearch/', views.AutoCompleteView.as_view(), name='autocompletesearch'),
    path('searchbox/', csrf_exempt(views.SearchBox.as_view()), name='searchbox'),
    path('copies_of_books/', views.CopiesOfBooks.as_view(), name='copies_of_books'),
    path('booklist', views.BookListView.as_view(), name='booklist'),
    path('bookdetail/<int:id>', views.BookDetailView.as_view(), name='bookdetail'),
    path('bookadd/', views.BookAddView.as_view(), name='bookadd'),
    path('bookupdate/<int:id>', views.BookUpdateView.as_view(), name='bookupdate'),
    path('bookdelete/<int:id>', views.BookDeleteView.as_view(), name='bookdelete'),

    path('viewtotalissuedbooks/', views.ViewTotalIssuedBooks.as_view(), name='viewtotalissuedbooks'),
    path('bookrecord/<int:id>/', views.BookIssueView.as_view(), name='bookrecord'),
    path('bookreturn/<int:id>/', views.BookReturnView.as_view(), name='bookreturn'),
]
