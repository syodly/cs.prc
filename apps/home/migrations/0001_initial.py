# Generated by Django 5.2.3 on 2025-06-18 06:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='发布日期')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否激活')),
                ('priority', models.IntegerField(default=0, help_text='数字越大优先级越高', verbose_name='优先级')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
                'ordering': ['-priority', '-date'],
            },
        ),
    ]
