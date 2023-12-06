from django.shortcuts import render,redirect
from .models import Book,WishList
from .forms import BookSearchForm
import user_authentication.urls
from transaction.models import Borrow
from django.contrib import messages 
from .forms import BookForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Create your views here.


def book_search(request):
    '''search book by book title or genre'''
    if not request.user.is_authenticated: 
        return redirect('login')   
    form = BookSearchForm(request.GET)
    books = Book.objects.all()
    search_query = None
    if request.method == 'GET' and form.is_valid():
        search_query = form.cleaned_data['search_query']
        if search_query:
            books = books.filter(Q(title__icontains=search_query) | Q(genre__icontains=search_query))
    user_borrowed_books = Borrow.objects.filter(user=request.user).values_list('book__isbn', flat=True)
    for book in books:
        book.is_already_borrowed = book.isbn in user_borrowed_books # check user already borrowed books for handle in frontend
    context = {'formse': form, 'books': books, 'search_query': search_query}
    return render(request, 'book_management/search_book_show.html', context)


def show_all_books(request):
    '''All Books list'''
    user = request.user

    books = Book.objects.all()
    user_borrowed_books = Borrow.objects.filter(user=user).values_list('book__isbn', flat=True)
    for book in books:
        book.is_already_borrowed = book.isbn in user_borrowed_books  # check book already borrowed for an user
    return render(request, 'book_management/show_books.html', {'books': books})


def request_book(request,isbn):
    '''if books not avilable then user can request for this books'''
    if not request.user.is_authenticated: 
        return redirect('login')
    if request.method == 'GET':
        messages.success(request, f'Your successfully Request book, ISBN Number is {isbn}')
    return redirect('profile')

# add in user wish list
def add_wish_list(request, isbn):
    '''add books in user wish list'''
    if not request.user.is_authenticated:
        return redirect('login')
    
    book = Book.objects.get(isbn=isbn)
    user = request.user
    
    try:
        wishlist = WishList.objects.get(user=user)
    except ObjectDoesNotExist:  
        wishlist = WishList.objects.create(user=user)
    
    if book not in wishlist.books.all():
        wishlist.books.add(book)
        messages.success(request, f'Book with ISBN: {isbn} has been added to your wishlist.')
    else:
        messages.warning(request, f'You already have the book with ISBN: {isbn} in your wishlist.')

    books = Book.objects.filter(wishlist__user=user).distinct()
    borrowed_isbns = Borrow.objects.filter(user=user).values_list('book__isbn', flat=True)
    for book in books:
        book.is_borrowed = book.isbn in borrowed_isbns
    return render(request, 'book_management/show_wish_list.html', {'books': books})

def show_all_wish_list(request):
    '''show all wish list book of user'''
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    books = Book.objects.filter(wishlist__user=user).distinct()
    borrowed_isbns = Borrow.objects.filter(user=user).values_list('book__isbn', flat=True)
    for book in books:
        book.is_borrowed = book.isbn in borrowed_isbns
    return render(request, 'book_management/show_wish_list.html', {'books': books})



def remove_book_from_wishlist(request,isbn):
    '''remove book from wish list'''
    if not request.user.is_authenticated: 
        return redirect('login')
    book = Book.objects.get(isbn=isbn)
    wishlists = WishList.objects.filter(user=request.user)
    for wishlist in wishlists:
        wishlist.books.remove(book)
    messages.warning(request, f'Your successfully removed book from Wsih list, ISBN: {isbn}')
    user=request.user
    books = Book.objects.filter(wishlist__user=user).distinct()
    return render(request,'book_management/show_wish_list.html',{'books':books})

def add_book(request):
    '''This feature for only admin can add books'''
    if not request.user.is_superuser: 
        return redirect('login')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_management:all-books')
    else:
        form = BookForm()
    return render(request,'book_management/add_book.html',{'form':form})
        
