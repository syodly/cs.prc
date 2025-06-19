from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_active', 'priority']
    list_filter = ['is_active', 'date']
    search_fields = ['title', 'content']
    date_hierarchy = 'date'
    ordering = ['-priority', '-date'] 