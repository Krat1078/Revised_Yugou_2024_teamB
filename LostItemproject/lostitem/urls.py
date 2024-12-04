from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'lostitem'  # 定义命名空间

urlpatterns = [
    path('', views.index, name='index'),
    path('restartPassword/', auth_views.PasswordResetView.as_view(),
             name='resetPassword'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('tolostitemregister/', views.tolostitemregister, name='tolostitemregister'),
    path('registeritem/', views.register_item, name='register_item'),
]