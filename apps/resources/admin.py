from django.contrib import admin
from .models import Book, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'isbn', 'publisher', 'quantity', 'created_at']
    search_fields = ['title', 'authors', 'isbn']
    list_filter = ['publisher', 'created_at']
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'parent']
    search_fields = ['code', 'name']
    list_filter = ['parent']
