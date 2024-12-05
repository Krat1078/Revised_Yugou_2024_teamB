from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'founditem'  # 定义命名空间

urlpatterns = [
    path('', views.index, name='index'),
    path('tofounditemregister/', views.tofounditemregister, name='tofounditemregister')
]