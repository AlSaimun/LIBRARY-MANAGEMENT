from django.contrib import admin
from .models import Book,WishList
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'available_status', 'num_of_copies')


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_books')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(books=None)
    
    def display_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])
    
admin.site.register(WishList, WishListAdmin)
