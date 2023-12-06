from django.db import models
from book_management.models import Book, User
from django.utils import timezone
# Create your models here.


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='borrowed_books', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(null= True, blank=True)
    is_already_borrowed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'book']
        
    def __str__(self) -> str:
        return f'{self.user} borrowed {self.book}'
    

    '''calculate fine'''
    def calculate_fine(self):
        current_date = timezone.now().date()
        days_difference = (current_date - self.return_date.date()).days

        fine_amount = max(0, days_difference * 5)

        return fine_amount
        

class PaymentGateWaySettings(models.Model):
    store_id = models.CharField(max_length=55)
    store_pass = models.CharField(max_length=55)