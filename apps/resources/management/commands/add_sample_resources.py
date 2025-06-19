from django.core.management.base import BaseCommand
from django.core.files import File
from apps.resources.models import Resource
import os
from django.conf import settings

class Command(BaseCommand):
    help = '添加示例资源数据'

    def handle(self, *args, **kwargs):
        # 示例图书数据
        books = [
            {
                'title': '追风筝的人',
                'author': '卡勒德·胡赛尼',
                'description': '12岁的阿富汗富家少爷阿米尔与仆人哈桑情同手足。然而，在一场风筝比赛后，发生了一件悲惨的事情，阿米尔为自己的懦弱感到自责和痛苦，逼走了哈桑，不久，自己也跟随父亲逃往美国。\n成年后的阿米尔始终无法原谅自己当年对哈桑的背叛。为了赎罪，他再次踏上暌违二十多年的故乡，希望能为不幸的好友尽最后一点心力，却发现一个惊天谎言，儿时的噩梦再度重演，阿米尔该如何抉择？',
                'category': '文学小说',
                'resource_type': 'book',
                'cover_image': 'book_covers/追风筝的人.png',
                'tags': '小说 成长 救赎',
            },
            {
                'title': '百年孤独',
                'author': '加西亚·马尔克斯',
                'description': '《百年孤独》是魔幻现实主义文学的代表作，描写了布恩迪亚家族七代人的传奇故事，以及加勒比海沿岸小镇马孔多的百年兴衰，反映了拉丁美洲的历史现实。',
                'category': '世界名著',
                'resource_type': 'book',
                'cover_image': 'book_covers/百年孤独.png',
                'tags': '魔幻现实主义 拉美文学 家族史诗',
            },
            {
                'title': '三体',
                'author': '刘慈欣',
                'description': '文化大革命期间，一次偶然的机会，南京大学物理系女青年叶文洁进入军方绝秘计划"红岸工程"。她的一个决定，导致了地球文明面临被三体文明毁灭的危险。',
                'category': '科幻小说',
                'resource_type': 'book',
                'cover_image': 'book_covers/三体.png',
                'tags': '科幻 硬科幻 三体',
            }
        ]

        # 添加示例图书
        for book_data in books:
            cover_path = book_data.pop('cover_image')
            # 检查资源是否已存在
            if not Resource.objects.filter(title=book_data['title']).exists():
                book = Resource.objects.create(**book_data)
                # 如果封面图片文件存在，则添加封面
                cover_full_path = os.path.join(settings.MEDIA_ROOT, cover_path)
                if os.path.exists(cover_full_path):
                    with open(cover_full_path, 'rb') as f:
                        book.cover_image.save(os.path.basename(cover_path), File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'成功添加图书: {book.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'图书已存在: {book_data["title"]}')) 