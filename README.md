
# 网络资源管理系统

## 项目简介
这是一个基于Django开发的图书馆资源管理系统，支持图书和其他资源的管理、借阅和下载功能。系统提供了用户管理、资源管理、借阅管理等完整的功能模块。

## 技术栈
- Python
- Django
- HTML/CSS
- Bootstrap

## 功能特点
- 用户管理
  - 用户注册和登录
  - 个人信息管理
  - 权限控制
- 资源管理
  - 图书和资源的添加、编辑、删除
  - 资源封面图片上传
  - 资源文件下载
  - 资源详情查看
- 借阅管理
  - 借阅申请
  - 借阅历史查看
  - 借阅状态追踪
- 主页功能
  - 公告管理
  - 系统信息展示

## 项目结构
```
cs.prc/
├── apps/                    # 应用程序目录
│   ├── borrowing/          # 借阅管理模块
│   ├── home/               # 主页模块
│   ├── resources/          # 资源管理模块
│   └── users/              # 用户管理模块
├── library_system/         # 项目配置目录
├── media/                  # 媒体文件目录
│   ├── book_covers/       # 图书封面存储
│   └── resource_covers/   # 资源封面存储
├── templates/              # HTML模板目录
└── manage.py              # Django管理脚本
```

## 安装和运行
1. 克隆项目到本地
```bash
git clone [项目地址]
```

2. 创建并激活虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 数据库迁移
```bash
python manage.py migrate
```

5. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

6. 运行开发服务器
```bash
python manage.py runserver
```

## 文件存储说明
- 资源文件存储在本地文件系统中
- 图书封面存储在 `/media/book_covers/` 目录
- 资源封面存储在 `/media/resource_covers/` 目录
- 资源文件按年月存储在 `/media/resources/YYYY/MM/` 目录

## 示例数据
系统提供了示例数据添加命令：
```bash
python manage.py add_sample_announcements  # 添加示例公告
python manage.py add_sample_resources     # 添加示例资源
```

## 注意事项
- 请确保media目录具有适当的写入权限
- 建议在生产环境中使用更安全的数据库（如MySQL）
- 生产环境部署时需要配置适当的静态文件服务
