from django.urls import path,include
from . import views

app_name = 'transaction'

urlpatterns = [
   path('borrow/<str:isbn>/', views.borrow_book, name='borrow-book'),
   path('return_book/<str:isbn>/', views.return_book, name='return-book'),
   path('show_borrow/', views.show_borrowed_books, name='show-borrow-book'),
   # path('fine/', views.pay_fine, name='pay-fine'),
   path('success/', views.success, name='success'),
   path('failled/', views.failed, name='failled'),
]