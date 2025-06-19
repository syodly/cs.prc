from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden, FileResponse
from .models import Resource
from .forms import ResourceForm

def resource_list(request):
    query = request.GET.get('q')
    resource_type = request.GET.get('type')
    
    resources = Resource.objects.filter(is_active=True)
    
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__icontains=query) |
            Q(tags__icontains=query)
        )
    
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    return render(request, 'resources/resource_list.html', {
        'resources': resources,
        'current_type': resource_type
    })

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {
        'resource': resource
    })

@login_required
def resource_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("您没有权限创建资源")
        
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save()
            messages.success(request, '资源创建成功！')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': '新增资源'
    })

@login_required
def resource_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("您没有权限编辑资源")
        
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            resource = form.save()
            messages.success(request, '资源更新成功！')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': '编辑资源'
    })

@login_required
def resource_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("您没有权限删除资源")
        
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, '资源删除成功！')
        return redirect('resources:resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {
        'resource': resource
    })

@login_required
def resource_download(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    # 检查用户下载限制
    if request.user.download_limit == 0:
        messages.error(request, '您今日的下载次数已达上限')
        return redirect('resources:resource_detail', pk=pk)
    
    # 更新下载次数
    resource.download_count += 1
    resource.save()
    
    # 如果用户不是管理员，减少下载限制
    if not request.user.is_staff and request.user.download_limit > 0:
        request.user.download_limit -= 1
        request.user.save()
    
    # 记录下载
    from .models import Download
    Download.objects.create(
        user=request.user,
        resource=resource,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # 返回文件
    response = FileResponse(resource.file)
    return response
