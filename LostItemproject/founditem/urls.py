from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'founditem'

urlpatterns = [
    path('', views.index, name='index'),
    path('tofounditemregister/', views.tofounditemregister, name='tofounditemregister'),
    path('registeritem/', views.register_item, name='register_item'),
    path('image/<int:id>/', views.get_image, name='get_image'),
    path('validate_qr_code', views.validate_qr_code, name='validate_qr_code'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
]
