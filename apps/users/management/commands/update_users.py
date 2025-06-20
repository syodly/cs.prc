from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '更新所有用户的类型和权限'

    def handle(self, *args, **options):
        self.stdout.write('开始更新用户...')
        User.update_all_users()
        self.stdout.write(self.style.SUCCESS('用户更新完成！')) 