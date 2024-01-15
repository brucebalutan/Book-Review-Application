from django.contrib import admin
from django.urls import path
from . import views

# Urls for reviews application
urlpatterns = [
    path('', views.index, name='Welcome View'),
    path('books/', views.books_list, name="Books List"),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('book-search/', views.book_search, name="Book Search"),
    path('email/', views.email, name="Email")
]