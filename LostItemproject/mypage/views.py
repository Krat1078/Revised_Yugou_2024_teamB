from django.shortcuts import render

# Create your views here.

def student_mypage(request):
    return render(request, "student.html")

def admin_mypage(request): # 未完成
    return render(request, "administrator.html")