from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.books.models import Book
from datetime import datetime

class Command(BaseCommand):
    help = '添加示例图书数据'

    def handle(self, *args, **kwargs):
        books_data = [
            {
                'title': '三体',
                'authors': '刘慈欣',
                'isbn': '9787536692930',
                'publisher': '重庆出版社',
                'publication_date': '2008-01-01',
                'introduction': '文化大革命期间，一个秘密军事项目向宇宙发出信号，意外引发了地球文明与三体文明的第一次接触...',
                'quantity': 10,
            },
            {
                'title': '活着',
                'authors': '余华',
                'isbn': '9787506365437',
                'publisher': '作家出版社',
                'publication_date': '2012-08-01',
                'introduction': '《活着》是余华最具代表性的作品之一，讲述了农村人福贵悲惨的人生遭遇...',
                'quantity': 8,
            },
            {
                'title': '百年孤独',
                'authors': '加西亚·马尔克斯',
                'isbn': '9787544253994',
                'publisher': '南海出版公司',
                'publication_date': '2011-06-01',
                'introduction': '《百年孤独》是魔幻现实主义文学的代表作，讲述了布恩迪亚家族七代人的故事...',
                'quantity': 5,
            },
            {
                'title': '围城',
                'authors': '钱钟书',
                'isbn': '9787020090006',
                'publisher': '人民文学出版社',
                'publication_date': '2012-09-01',
                'introduction': '《围城》是钱钟书所著的长篇小说，描写了青年知识分子婚姻和事业的烦恼...',
                'quantity': 7,
            },
            {
                'title': '平凡的世界',
                'authors': '路遥',
                'isbn': '9787530216781',
                'publisher': '北京十月文艺出版社',
                'publication_date': '2017-06-01',
                'introduction': '《平凡的世界》是一部全景式地展示中国当代城乡社会生活的长篇小说...',
                'quantity': 12,
            },
            {
                'title': '红楼梦',
                'authors': '曹雪芹',
                'isbn': '9787020002207',
                'publisher': '人民文学出版社',
                'publication_date': '1996-12-01',
                'introduction': '《红楼梦》是一部百科全书式的长篇小说，描绘了贾、史、王、薛四大家族的兴衰...',
                'quantity': 6,
            },
            {
                'title': '1984',
                'authors': '乔治·奥威尔',
                'isbn': '9787530210291',
                'publisher': '北京十月文艺出版社',
                'publication_date': '2010-04-01',
                'introduction': '《1984》是一部反乌托邦小说，描绘了一个极权主义社会的可怕景象...',
                'quantity': 9,
            },
            {
                'title': '追风筝的人',
                'authors': '卡勒德·胡赛尼',
                'isbn': '9787208061644',
                'publisher': '上海人民出版社',
                'publication_date': '2006-05-01',
                'introduction': '《追风筝的人》讲述了阿富汗富家少爷阿米尔与仆人哈桑之子之间的故事...',
                'quantity': 15,
            }
        ]

        for book_data in books_data:
            # 将日期字符串转换为日期对象
            book_data['publication_date'] = datetime.strptime(
                book_data['publication_date'], '%Y-%m-%d'
            ).date()
            
            # 检查ISBN是否已存在
            if not Book.objects.filter(isbn=book_data['isbn']).exists():
                Book.objects.create(**book_data)
                self.stdout.write(
                    self.style.SUCCESS(f'成功添加图书: {book_data["title"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'图书已存在，跳过: {book_data["title"]}')
                )

        self.stdout.write(self.style.SUCCESS('示例图书添加完成！')) 