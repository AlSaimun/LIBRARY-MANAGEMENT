from django import forms
from .models import Book


class BookSearchForm(forms.Form):
    search_query = forms.CharField(label="Search Books",required=False,widget=forms.TextInput(attrs={"placeholder": "Enter book title or genre"}))
    

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','genre','author','image_url','isbn','num_of_copies',]
        widgets ={'genre':forms.TextInput(attrs={'placeholder':'Story,Novel,etc'})}
