from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('guest', '访客'),
        ('registered', '注册用户'),
        ('admin', '管理员'),
    )
    
    user_type = models.CharField('用户类型', max_length=10, choices=USER_TYPE_CHOICES, default='guest')
    phone_regex = RegexValidator(
        regex=r'^1[3-9]\d{9}$',
        message='请输入有效的手机号码'
    )
    phone = models.CharField('手机号码', max_length=11, validators=[phone_regex], blank=True, null=True)
    email = models.EmailField('邮箱', max_length=254, blank=True)
    download_limit = models.IntegerField('每日下载限制', default=5)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        # 根据用户类型设置下载限制
        if not self.pk:  # 只在创建时设置
            if self.user_type == 'guest':
                self.download_limit = 2
            elif self.user_type == 'registered':
                self.download_limit = 10
            elif self.user_type == 'admin':
                self.download_limit = -1  # -1表示无限制
        super().save(*args, **kwargs)
