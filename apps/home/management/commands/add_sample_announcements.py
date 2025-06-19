from django.core.management.base import BaseCommand
from apps.home.models import Announcement
from django.utils import timezone

class Command(BaseCommand):
    help = '添加示例公告数据'

    def handle(self, *args, **kwargs):
        announcements = [
            {
                'title': '图书馆开放时间调整通知',
                'content': '亲爱的读者：\n为了更好地服务广大师生，图书馆开放时间调整如下：\n周一至周五：8:00-22:00\n周六至周日：9:00-21:00',
                'priority': 3,
            },
            {
                'title': '新书推荐',
                'content': '本月新增图书100余册，包括计算机科学、文学艺术、自然科学等多个领域的优秀著作。欢迎借阅！',
                'priority': 2,
            },
            {
                'title': '图书馆电子资源使用讲座',
                'content': '为帮助读者更好地利用图书馆电子资源，我们将于本周五下午2点在图书馆多媒体室举办使用讲座，欢迎参加！',
                'priority': 1,
            },
        ]

        for announcement_data in announcements:
            Announcement.objects.create(**announcement_data)

        self.stdout.write(self.style.SUCCESS('成功添加示例公告！')) 