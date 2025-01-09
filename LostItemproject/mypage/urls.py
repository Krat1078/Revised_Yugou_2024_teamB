from django.urls import path
from mypage import views
from django.contrib import admin # 一時的

app_name = "mypage"

urlpatterns = [
    # path("admin/", admin.site.urls), # 管理者がマイページに行くとadmin管理画面に行く（一時的）
    path("student/", views.student_mypage, name="student_mypage"), # 学生マイページ表示
    path("student_delete/<int:item_id>/", views.student_delete, name="student_delete"), # 学生マイページデータ削除
    path("administrator", views.admin_mypage, name="admin_mypage"),
]