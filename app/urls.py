from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books, name='books'),
    path('book_details/<str:book_id>/', views.book_details, name='book_details'),
    path('images/', views.images, name='images'),
    path('image_details/<int:image_id>/', views.image_details, name='image_details'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/<str:book_id>/', views.delete_cart, name='delete_cart'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('about/', views.about, name='about'),
    path('contect/', views.contect, name='contect')
] 