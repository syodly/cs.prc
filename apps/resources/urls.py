from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('<int:pk>/', views.resource_detail, name='resource_detail'),
    path('create/', views.resource_create, name='resource_create'),
    path('<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('<int:pk>/delete/', views.resource_delete, name='resource_delete'),
    path('<int:pk>/download/', views.resource_download, name='resource_download'),
]
