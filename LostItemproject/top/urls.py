from django.urls import path
from . import views

app_name = 'top'  # 定义命名空间

urlpatterns = [
    path('', views.index, name='index'),
]