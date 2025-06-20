from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 如果用户不是管理员，移除管理员专用字段
        if user and not user.is_staff:
            self.fields.pop('is_featured', None)
            self.fields.pop('is_active', None)
            self.fields.pop('status', None)
    
    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_type', 'file', 'cover_image', 
                 'author', 'category', 'tags', 'is_featured', 'is_active', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '使用逗号分隔多个标签'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        } 