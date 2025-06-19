from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.resources.models import Resource

class BorrowRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='资源')
    borrow_date = models.DateTimeField('借阅时间', default=timezone.now)
    due_date = models.DateTimeField('应还时间')
    return_date = models.DateTimeField('归还时间', null=True, blank=True)
    returned = models.BooleanField('是否已归还', default=False)
    
    class Meta:
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"

    @property
    def is_overdue(self):
        if not self.returned and timezone.now() > self.due_date:
            return True
        return False 