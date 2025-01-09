from django.shortcuts import render, get_object_or_404, redirect
from top.models import Item

# Create your views here.

def student_mypage(request): # 表示用ビュー
    username = request.user.username # ユーザー名の取得
    useritems = Item.objects.filter(contact_email__startswith=username, item_type=1) 
    return render(request, "student.html", {"useritems":useritems})

def student_delete(request, item_id): # 削除用ビュー
    if request.method == "POST":
        item = get_object_or_404(Item, item_id=item_id)
        item.delete()
        return redirect("mypage:student_mypage")


def admin_mypage(request): # 未完成
    username = request.user.username # ユーザー名の取得
    founditems = Item.objects.filter(item_type=0).order_by("created_at") 
    return render(request, "administrator.html", {"founditems":founditems})