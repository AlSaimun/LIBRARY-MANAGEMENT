from django.shortcuts import render,redirect
from .models import Borrow,Book
from django.contrib import messages 
from django.db.models import Q
from django.utils import timezone
from .ssl import sslcommerz_payment_gateway
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def borrow_book(request,isbn):
    '''borrow a book'''
    if not request.user.is_authenticated:
        return redirect('login')
    book = Book.objects.get(isbn=isbn)
    user = request.user
    borrow_obj,created = Borrow.objects.get_or_create(user=user,book=book)
    if created:
        borrow_obj.return_date = timezone.now() + timezone.timedelta(days=15)
        # borrow_obj.return_date = timezone.now() + timezone.timedelta(days=1) #for testing
        borrow_obj.save() 
        book.num_of_copies -= 1
        book.save()
        messages.success(request,"Borrowed Successfully")
    else:
        messages.warning(request,"Borrowed unsuccessfull")
    return redirect('transaction:show-borrow-book')
    




def show_borrowed_books(request):
    '''show all borrwed books'''
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    borrowed_books = Book.objects.filter(borrowed_books__user=user).distinct().exclude(isbn='').order_by('borrowed_books__return_date')
    return render(request, 'transaction/show_all_borrow_book.html', {'books': borrowed_books})  

def return_book(request, isbn):
    '''User return a book'''
    if not request.user.is_authenticated:
        return redirect('login') 
    try:
        borrow_obj = Borrow.objects.get(Q(book__isbn=isbn) & Q(user=request.user))
    except Borrow.DoesNotExist:
        return render(request, 'transaction/test.html', {'mes': "Borrow record not found"})
    print(borrow_obj.calculate_fine())
    fine = borrow_obj.calculate_fine()
    borrow_obj.delete() # delete obj
    try:
        book = Book.objects.get(isbn=isbn)
        book.num_of_copies += 1
        book.save()
    except Book.DoesNotExist:
        return render(request, 'transaction/test.html', {'mes': "Book not found"})
    if fine > 0:
        return redirect(sslcommerz_payment_gateway(request, fine)) # redirect to sslcommerze page

    messages.success(request, "You Successfully Return book")
    return redirect('transaction:show-borrow-book')


@csrf_exempt
def success(request):
    '''Payment successfull'''
    print(request.POST)
    messages.success(request, "You have successfully paid the fine.")
    return redirect('transaction:show-borrow-book')

@csrf_exempt
def failed(request):
    '''Payment unsuccessfull'''
    messages.success(request, "Payment unsuccessfull.")
    return redirect('transaction:show-borrow-book')
