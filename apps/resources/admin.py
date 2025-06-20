from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'resource_type', 'category', 'download_count', 'upload_date', 'is_featured', 'is_active']
    search_fields = ['title', 'author', 'description', 'tags']
    list_filter = ['resource_type', 'category', 'is_featured', 'is_active']
    date_hierarchy = 'upload_date'
