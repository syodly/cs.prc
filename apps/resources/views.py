from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden, FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
import os
import mimetypes
from urllib.parse import quote
from .models import Resource
from .forms import ResourceForm

def resource_list(request):
    query = request.GET.get('q')
    resource_type = request.GET.get('type')
    
    # 只显示已通过审核的资源
    resources = Resource.objects.filter(is_active=True, status='approved')
    
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
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = request.user
            resource.status = 'pending'
            resource.is_active = False
            resource.save()
            messages.success(request, '资源上传成功！请等待管理员审核。')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm(user=request.user)
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': '上传资源'
    })

@login_required
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    # 检查权限
    if not request.user.is_staff and request.user != resource.uploader:
        return HttpResponseForbidden("您没有权限编辑此资源")
        
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource, user=request.user)
        if form.is_valid():
            resource = form.save(commit=False)
            if not request.user.is_staff:
                resource.status = 'pending'  # 非管理员修改后需要重新审核
                resource.is_active = False
            resource.save()
            messages.success(request, '资源更新成功！' + ('' if request.user.is_staff else '请等待管理员审核。'))
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm(instance=resource, user=request.user)
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
    
    # 获取文件路径和文件名
    file_path = resource.file.path
    original_filename = os.path.basename(resource.file.name)
    
    # 获取文件的MIME类型
    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # 打开文件并创建响应
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            
            # 添加下载头
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(original_filename)}'
            response['Content-Length'] = os.path.getsize(file_path)
            
            # 添加缓存控制头
            response['Cache-Control'] = 'no-cache'
            
            return response
    except FileNotFoundError:
        messages.error(request, '文件不存在或已被删除')
        return redirect('resources:resource_detail', pk=pk)
    except Exception as e:
        messages.error(request, f'下载出错：{str(e)}')
        return redirect('resources:resource_detail', pk=pk)

@user_passes_test(lambda u: u.is_staff)
def pending_resources(request):
    pending_resources = Resource.objects.filter(status='pending').order_by('-upload_date')
    return render(request, 'resources/pending_resources.html', {
        'pending_resources': pending_resources
    })

@user_passes_test(lambda u: u.is_staff)
def approve_resource(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    resource = get_object_or_404(Resource, pk=pk)
    resource.status = 'approved'
    resource.is_active = True
    resource.save()
    
    messages.success(request, f'资源 "{resource.title}" 已通过审核')
    return JsonResponse({'status': 'success'})

@user_passes_test(lambda u: u.is_staff)
def reject_resource(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    resource = get_object_or_404(Resource, pk=pk)
    resource.status = 'rejected'
    resource.is_active = False
    resource.save()
    
    messages.success(request, f'资源 "{resource.title}" 已被拒绝')
    return JsonResponse({'status': 'success'})
