from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    date = models.DateField('发布日期', default=timezone.now)
    is_active = models.BooleanField('是否激活', default=True)
    priority = models.IntegerField('优先级', default=0, help_text='数字越大优先级越高')

    class Meta:
        ordering = ['-priority', '-date']
        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):
        return self.title 