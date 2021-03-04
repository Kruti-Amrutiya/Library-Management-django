from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view.as_view(), name='home'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('studentprofile', views.StudentProfileView.as_view(), name='studentprofile'),
    path('librarianprofile', views.LibrarianProfileView.as_view(), name='librarianprofile'),
    path('adminprofile', views.AdminProfileView.as_view(), name='adminprofile'),
    path('bookindex', views.BookIndexView.as_view(), name='bookindex'),
    path('bookadd/', views.BookAddView.as_view(), name='bookadd'),
    path('bookupdate/<int:id>', views.BookUpdateView.as_view(), name='bookupdate'),
    path('bookdelete/<int:id>', views.BookDeleteView.as_view(), name='bookdelete'),
    path('bookissued', views.BookIndexView.as_view(), name='bookissued'),
    path('viewissuedbookbystudent/', views.ViewIssuedBooksByStudent.as_view(), name='viewissuedbookbystudent'),
    path('viewissuedbooks/', views.ViewIssuedBooks.as_view(), name='viewissuedbooks'),
    # path('viewissuedbooksrequest/', views.ViewIssuedBooksRequest.as_view(), name='viewissuedbooksrequest'),
]
