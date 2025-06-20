from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('registered', '普通用户'),
        ('admin', '管理员'),
    )
    
    user_type = models.CharField('用户类型', max_length=10, choices=USER_TYPE_CHOICES, default='registered')
    phone_regex = RegexValidator(
        regex=r'^1[3-9]\d{9}$',
        message='请输入有效的手机号码'
    )
    phone = models.CharField('手机号码', max_length=11, validators=[phone_regex], blank=True, null=True)
    email = models.EmailField('邮箱', max_length=254, blank=True)
    download_limit = models.IntegerField('每日下载限制', default=20)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        # 设置用户类型和下载限制
        if self.is_superuser:
            self.user_type = 'admin'
            self.download_limit = -1
        elif not self.pk:  # 新用户但不是超级用户
            self.user_type = 'registered'
            self.download_limit = 20
        
        # 确保管理员始终有无限下载权限
        if self.is_superuser or self.user_type == 'admin':
            self.download_limit = -1
            
        super().save(*args, **kwargs)

    @property
    def download_limit_display(self):
        """返回用户下载限制的显示文本"""
        if self.is_superuser or self.user_type == 'admin':
            return '无限制'
        return f'{self.download_limit} 次'

    @classmethod
    def update_all_users(cls):
        """更新所有用户的类型和权限"""
        for user in cls.objects.all():
            if user.is_superuser:
                user.user_type = 'admin'
                user.download_limit = -1
            else:
                user.user_type = 'registered'
                user.download_limit = 20
            user.save()
