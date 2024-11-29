from django.urls import path
from . import views

app_name = 'top'  # 名前空間の定義

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home')
]