from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '检查用户数据'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            self.stdout.write(f"用户名: {user.username}")
            self.stdout.write(f"用户类型: {user.user_type}")
            self.stdout.write(f"是否是超级用户: {user.is_superuser}")
            self.stdout.write(f"下载限制: {user.download_limit}")
            self.stdout.write("-------------------") 