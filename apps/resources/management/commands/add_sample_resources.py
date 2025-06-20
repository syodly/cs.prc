from django.core.management.base import BaseCommand
from django.core.files import File
from apps.resources.models import Resource
import os
from django.conf import settings
from django.utils import timezone

class Command(BaseCommand):
    help = '添加示例资源数据'

    def handle(self, *args, **kwargs):
        # 示例资源数据
        resources = [
            {
                'title': '追风筝的人',
                'author': '卡勒德·胡赛尼',
                'description': '12岁的阿富汗富家少爷阿米尔与仆人哈桑情同手足。然而，在一场风筝比赛后，发生了一件悲惨的事情，阿米尔为自己的懦弱感到自责和痛苦，逼走了哈桑，不久，自己也跟随父亲逃往美国。',
                'category': '文学小说',
                'resource_type': 'book',
                'cover_image': 'resource_covers/追风筝的人.png',
                'tags': '小说,成长,救赎',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '高等数学期末试卷',
                'author': '数学教研室',
                'description': '2024年春季学期高等数学期末考试真题及答案',
                'category': '考试资源',
                'resource_type': 'exam',
                'tags': '高数,期末,试卷',
                'is_featured': False,
                'is_active': True,
            },
            {
                'title': '计算机网络教材',
                'author': '谢希仁',
                'description': '本书是计算机网络专业本科教材，全面介绍了计算机网络的基本原理和技术。',
                'category': '教材',
                'resource_type': 'textbook',
                'cover_image': 'resource_covers/计算机网络.jpg',
                'tags': '计算机网络,教材,本科',
                'is_featured': True,
                'is_active': True,
            },
            # 新增9本电子图书
            {
                'title': '百年孤独',
                'author': '加西亚·马尔克斯',
                'description': '《百年孤独》是魔幻现实主义文学的代表作，描写了布恩迪亚家族七代人的传奇故事，以及加勒比海沿岸小镇马孔多的百年兴衰。',
                'category': '世界名著',
                'resource_type': 'book',
                'cover_image': 'resource_covers/百年孤独.jpg',
                'tags': '魔幻现实主义,拉美文学,经典',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '三体',
                'author': '刘慈欣',
                'description': '文化大革命期间，一次偶然的机会，南京大学物理系女青年叶文洁进入军方绝秘计划"红岸工程"。她的一个决定，导致了地球文明面临被三体文明毁灭的危险。',
                'category': '科幻小说',
                'resource_type': 'book',
                'cover_image': 'resource_covers/三体.jpg',
                'tags': '科幻,硬科幻,中国科幻',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '活着',
                'author': '余华',
                'description': '《活着》是余华最具代表性的作品。讲述了农村人福贵悲惨的人生遭遇。福贵先是富少爷，后来一贫如洗，被抓去当兵，回来后当农民，在"大跃进"期间，更是不得不送掉自己的儿子。',
                'category': '文学小说',
                'resource_type': 'book',
                'cover_image': 'resource_covers/活着.jpg',
                'tags': '当代文学,人性,苦难',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '1984',
                'author': '乔治·奥威尔',
                'description': '《1984》是一部反乌托邦小说，描绘了一个极权主义统治的社会。在这个社会中，人们在老大哥的持续监视下生活，言论、思想都受到严格控制。',
                'category': '世界名著',
                'resource_type': 'book',
                'cover_image': 'resource_covers/1984.jpg',
                'tags': '反乌托邦,政治寓言,经典',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '围城',
                'author': '钱钟书',
                'description': '《围城》是钱钟书所著的长篇小说，描写了青年知识分子方鸿渐从美国留学回来后的故事。小说以结婚为核心，从婚姻的角度展现了在社会变革时期知识分子的生活。',
                'category': '文学小说',
                'resource_type': 'book',
                'cover_image': 'resource_covers/围城.jpg',
                'tags': '讽刺,知识分子,婚姻',
                'is_featured': False,
                'is_active': True,
            },
            {
                'title': '平凡的世界',
                'author': '路遥',
                'description': '《平凡的世界》是一部现实主义小说，描写了陕北黄土高原上的普通农民孙少安和孙少平两兄弟为改变命运而奋斗的故事。',
                'category': '文学小说',
                'resource_type': 'book',
                'cover_image': 'resource_covers/平凡的世界.jpg',
                'tags': '现实主义,农村,奋斗',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '红楼梦',
                'author': '曹雪芹',
                'description': '《红楼梦》是一部百科全书式的长篇小说，以贾宝玉、林黛玉、薛宝钗的爱情婚姻悲剧为主线，描绘了贾、史、王、薛四大家族的兴衰。',
                'category': '古典文学',
                'resource_type': 'book',
                'cover_image': 'resource_covers/红楼梦.jpg',
                'tags': '古典,爱情,家族',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '人类简史',
                'author': '尤瓦尔·赫拉利',
                'description': '《人类简史》是一部跨学科的人类历史著作，从生物学、人类学、经济学等多个角度，讲述了人类从智人时代到21世纪的发展历程。',
                'category': '科普读物',
                'resource_type': 'book',
                'cover_image': 'resource_covers/人类简史.jpg',
                'tags': '历史,人类学,科普',
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': '解忧杂货店',
                'author': '东野圭吾',
                'description': '《解忧杂货店》是东野圭吾的奇幻温情小说。在一家僻静街道上的杂货店，只要写下烦恼投进店前的邮箱，第二天就会在店后的牛奶箱里得到回答。',
                'category': '文学小说',
                'resource_type': 'book',
                'cover_image': 'resource_covers/解忧杂货店.jpg',
                'tags': '治愈,温情,日本文学',
                'is_featured': False,
                'is_active': True,
            }
        ]

        # 添加示例资源
        for resource_data in resources:
            # 获取并移除封面图片路径（如果存在）
            cover_path = resource_data.pop('cover_image', None)
            
            # 检查资源是否已存在
            if not Resource.objects.filter(title=resource_data['title']).exists():
                # 添加上传时间
                resource_data['upload_date'] = timezone.now()
                
                # 创建资源
                resource = Resource.objects.create(**resource_data)
                
                # 如果有封面图片且文件存在，则添加封面
                if cover_path:
                    cover_full_path = os.path.join(settings.MEDIA_ROOT, cover_path)
                    if os.path.exists(cover_full_path):
                        with open(cover_full_path, 'rb') as f:
                            resource.cover_image.save(
                                os.path.basename(cover_path),
                                File(f),
                                save=True
                            )
                
                self.stdout.write(
                    self.style.SUCCESS(f'成功添加资源: {resource.title} ({resource.get_resource_type_display()})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'资源已存在: {resource_data["title"]}')
                ) 