from django.urls import path
from mypage import views
from django.contrib import admin # 一時的

app_name = "mypage"

urlpatterns = [
    path("admin/", admin.site.urls), # 管理者がマイページに行くとadmin管理画面に行く（一時的）
    path("student/", views.student_mypage, name="student_mypage"),
    path("administrator", views.admin_mypage, name="admin_mypage"),
]