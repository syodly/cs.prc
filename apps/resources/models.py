from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Book(models.Model):
    title = models.CharField('书名', max_length=200)
    authors = models.CharField('作者', max_length=200)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    publisher = models.CharField('出版社', max_length=200)
    publication_date = models.DateField('出版日期')
    introduction = models.TextField('简介')
    cover = models.ImageField('封面', upload_to='book_covers/', null=True, blank=True)
    quantity = models.PositiveIntegerField('库存数量', default=0)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Category(models.Model):
    code = models.CharField('分类编码', max_length=20, unique=True)
    name = models.CharField('分类名称', max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父分类')
    
    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'

    def __str__(self):
        return self.name

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('book', '电子图书'),
        ('exam', '试卷资源'),
        ('textbook', '电子教材'),
    )

    title = models.CharField('标题', max_length=200)
    description = models.TextField('描述')
    resource_type = models.CharField('资源类型', max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField('资源文件', upload_to='resources/%Y/%m/')
    cover_image = models.ImageField('封面图片', upload_to='resource_covers/', null=True, blank=True)
    author = models.CharField('作者/出版社', max_length=200)
    upload_date = models.DateTimeField('上传时间', default=timezone.now)
    download_count = models.IntegerField('下载次数', default=0)
    category = models.CharField('分类', max_length=100)
    tags = models.CharField('标签', max_length=200, help_text='使用逗号分隔多个标签', blank=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    is_active = models.BooleanField('是否可用', default=True)

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = '资源'
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.get_resource_type_display()} - {self.title}"

class ResourceCategory(models.Model):
    name = models.CharField('分类名称', max_length=100)
    description = models.TextField('分类描述', blank=True)
    parent = models.ForeignKey('self', verbose_name='父分类', null=True, blank=True, on_delete=models.CASCADE)
    order = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '资源分类'
        verbose_name_plural = '资源分类'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Download(models.Model):
    user = models.ForeignKey('users.User', verbose_name='用户', on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, verbose_name='资源', on_delete=models.CASCADE)
    download_time = models.DateTimeField('下载时间', default=timezone.now)
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)

    class Meta:
        verbose_name = '下载记录'
        verbose_name_plural = '下载记录'
        ordering = ['-download_time']

    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"
