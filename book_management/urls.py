from django.urls import path,include
from . import views

app_name = 'book_management'

urlpatterns = [
   path('search/', views.book_search, name='book-search'),
   path('allBooks/', views.show_all_books, name='all-books'),
   path('add_book/', views.add_book, name='add-books'),
   path('request/<str:isbn>/', views.request_book, name='request'),
   path('add_list/<str:isbn>/', views.add_wish_list, name='add-wish-list'),
   path('show_wish_list/', views.show_all_wish_list, name='show-wish-list'),
   path('remove_wish_book/<str:isbn>/', views.remove_book_from_wishlist, name='remove-wish-book'),
]
