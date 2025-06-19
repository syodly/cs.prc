from django.contrib import admin
from .models import BorrowRecord

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'borrow_date', 'due_date', 'return_date', 'returned']
    list_filter = ['returned', 'borrow_date', 'due_date', 'return_date']
    search_fields = ['user__username', 'resource__title']
    date_hierarchy = 'borrow_date' 