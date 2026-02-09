from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='books'),
    path('add-book/', views.add_book, name='add_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow'),
    path('my-books/', views.my_books, name='my_books'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
]
