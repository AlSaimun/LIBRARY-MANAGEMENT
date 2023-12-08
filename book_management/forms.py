from typing import Any
from django import forms
from .models import Book
  

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','genre','author','image_url','isbn','num_of_copies',]
        widgets ={'genre':forms.TextInput(attrs={'placeholder':'Story,Novel,etc'})}
