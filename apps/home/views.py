from django.shortcuts import render
from .models import Announcement
from apps.resources.models import Resource

def home(request):
    """
    主页视图，显示公告和最新资源
    """
    announcements = Announcement.objects.filter(is_active=True)[:5]  # 获取最新的5条公告
    latest_resources = Resource.objects.filter(is_active=True).order_by('-upload_date')[:6]  # 获取最新上传的6个资源
    
    return render(request, 'home/home.html', {
        'announcements': announcements,
        'latest_resources': latest_resources,
    }) 