from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

  
class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    image_url = models.URLField(default='www.')
    isbn = models.CharField(primary_key=True,max_length=13,help_text="must be 13 character")
    publication_date = models.DateField(auto_now_add=True)
    available_status = models.BooleanField(default=True)
    num_of_copies = models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        if self.num_of_copies == 0:
            self.available_status = False
        else:
            self.available_status = True
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'{self.title}'
    
 
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
        
    def __str__(self):
        return f'Name: {self.user.username} - {", ".join([book.title for book in self.books.all()])}'
