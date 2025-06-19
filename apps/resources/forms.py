from django import forms
from .models import Book, Category, Resource

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'isbn', 'publisher', 'publication_date', 
                 'introduction', 'cover', 'quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'authors': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'introduction': forms.Textarea(attrs={'rows': 4}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if self.instance.pk is None:  # 只在创建新书时检查
            if Book.objects.filter(isbn=isbn).exists():
                raise forms.ValidationError('该ISBN已存在')
        return isbn 

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_type', 'file', 'cover_image', 
                 'author', 'category', 'tags', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': '使用逗号分隔多个标签'})
        } 