from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import BorrowRecord
from apps.resources.models import Resource

@login_required
def my_borrowings(request):
    borrowings = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'borrowing/my_borrowings.html', {'borrowings': borrowings})

@login_required
def borrow_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    user = request.user
    
    # 检查用户是否已达到最大借阅数量
    current_borrowed = BorrowRecord.objects.filter(user=user, returned=False).count()
    if current_borrowed >= user.max_books:
        messages.error(request, f'您已达到最大借阅数量限制（{user.max_books}本）')
        return redirect('resources:resource_detail', pk=pk)
    
    if request.method == 'POST':
        # 创建借阅记录
        from datetime import datetime, timedelta
        
        due_date = timezone.now() + timedelta(days=30)  # 设置30天的借阅期限
        
        BorrowRecord.objects.create(
            user=user,
            resource=resource,
            due_date=due_date
        )
        
        messages.success(request, f'成功借阅《{resource.title}》，请在{due_date.strftime("%Y-%m-%d")}前归还')
        return redirect('resources:resource_detail', pk=pk)
    
    return redirect('resources:resource_detail', pk=pk)

@login_required
def return_resource(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.returned = True
        record.return_date = timezone.now()
        record.save()
        messages.success(request, f'成功归还《{record.resource.title}》')
        return redirect('borrowing:my_borrowings')
    return redirect('borrowing:my_borrowings') 