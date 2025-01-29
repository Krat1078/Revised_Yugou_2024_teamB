from django.shortcuts import render, get_object_or_404, redirect
from top.models import Item, ItemImage, StorageLocationsTag

# Create your views here.

def student_mypage(request): # 表示用ビュー
    username = request.user.username # ユーザー名の取得
    useritems = Item.objects.filter(contact_email__startswith=username, item_type=1) 
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items") # チェックボックスで選択されたitem一覧
        print(selected_ids)
        Item.objects.filter(item_id__in=selected_ids).delete() # チェックボックスで選択したitemを削除
            
        return redirect("mypage:student_mypage")
    
    return render(request, "student.html", {"useritems":useritems})


def admin_mypage(request): # 未完成
    # username = request.user # ユーザー名の取得
    # founditems = Item.objects.filter(item_type=0).order_by("created_at") 
    founditemimages = ItemImage.objects.select_related("item").order_by("item__created_at")
    founditemimages = founditemimages.filter(item__status=0) # status = 0の物品だけ表示
    # founditem_ids = founditemimages.values_list("item__item_id", flat=True) # 拾得物のID取得
    storage_tags = StorageLocationsTag.objects.all()
    if request.method == "POST":

        action = request.POST.get("action") # 機能によってPOSTリクエストの遷移を変えるためのaction
        selected_ids = request.POST.getlist("selected_items") # チェックボックスで選択されたitem一覧

        if action == "search": # ID検索機能
            search_ID = request.POST.get("IDsearch")
            if search_ID == "":
                pass
            else:
                search_ID = int(search_ID) # item_idのデータ型はint
                founditemimages = founditemimages.filter(item__item_id=search_ID)

        elif action == "delete": # データ削除機能
            print(selected_ids)
            Item.objects.filter(item_id__in=selected_ids).delete() # チェックボックスで選択したitemを削除
            
            return redirect("mypage:admin_mypage")
        
        elif action == "search_location":
            if request.POST.get("search_location") == "":
                pass
            else:
                location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("search_location"))
                founditemimages = founditemimages.filter(item__storage_location=location)
            
        
        elif action == "change_location": # 保管場所変更機能
            before_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("before_location"))
            after_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("after_location"))
            # before_storageID = before_location.storage_location_id
            # after_storageID = after_location.storage_location_id
            change_items = founditemimages.filter(item__storage_location=before_location)
            for change_item in change_items:
                change_item.item.storage_location = after_location
                change_item.item.save()

            return redirect("mypage:admin_mypage")
        
        """
        修正箇所
        登録日時によって降順、昇順を選択できるようにする
        ページネーションの実装
        画面サイズを変えるとチェックボックスの選択内容が保持されない -> 各画面サイズによってチェックボックスの値を保持している状態である
        画像の大きさによってセルの大きさが変化してしまっているので、モーダル表示などで対応したい
        """
        

    return render(request, "administrator.html", {"founditemimages": founditemimages, "storagetags": storage_tags})