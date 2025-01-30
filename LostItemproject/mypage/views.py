from django.shortcuts import render, get_object_or_404, redirect
from top.models import Item, ItemImage, StorageLocationsTag
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def student_mypage(request): # 表示用ビュー
    username = request.user.username # ユーザー名の取得
    useritems = Item.objects.filter(contact_email=request.user.email, item_type=1) 
    
    return render(request, "student.html", {"useritems":useritems})


@csrf_exempt
def delete_item(request, item_id):
    print(f"Received DELETE request for item ID: {item_id}")  # デバッグ用出力

    if request.method == "POST":
        try:
            item = Item.objects.get(item_id=item_id)  # ここでエラーが出ていないか確認
            print(f"Deleting item: {item}")  # 取得したデータを表示
            item.delete()
            return JsonResponse({"success": True})
        except Item.DoesNotExist:
            print("Error: Item does not exist")
            return JsonResponse({"success": False, "error": "データが存在しません"}, status=404)
        except Exception as e:
            print(f"Unexpected error: {e}")  # 予期しないエラーをキャッチ
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    print("Error: Invalid request method")
    return JsonResponse({"success": False, "error": "無効なリクエスト"}, status=400)

def admin_mypage(request): 

    search_ID = ""

    if request.method == "POST":

        action = request.POST.get("action") # 機能によってPOSTリクエストの遷移を変えるためのaction
        selected_ids = request.POST.getlist("selected_items") # チェックボックスで選択されたitem一覧
        #request.session["selected_location"] = request.POST.get("search_location")  # 保管場所をセッションに保存

        if action == "search": # ID検索機能
            search_ID = request.POST.get("IDsearch")
        
        elif action == "search_location":
            request.session["selected_location"] = request.POST.get("search_location")  # 保管場所をセッションに保存
        
        elif action == "change_location": # 保管場所変更機能
            if request.POST.get("before_location") == "":
                pass
            else:
                before_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("before_location"))
                after_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("after_location"))
                founditemimages = ItemImage.objects.select_related("item").order_by("item__created_at")
                change_items = founditemimages.filter(item__storage_location=before_location)
                for change_item in change_items:
                    change_item.item.storage_location = after_location
                    change_item.item.save()

                return redirect("mypage:admin_mypage")

        elif action == "change_order":
            order = request.session.get("order", "asc") # セッションから現在のorderを取得。デフォルトは'asc'
            if order == "asc":
                #founditemimages = founditemimages.order_by("-item__created_at")
                next_order = "des"
            elif order == "des":
                #founditemimages = founditemimages.order_by("item__created_at")
                next_order = "asc"

            # 次回の順序をセッションに保存
            request.session['order'] = next_order
        
        """
        elif action == "delete": # データ削除機能
            print(selected_ids)
            if len(selected_ids) == 0:
                pass
            else:
                Item.objects.filter(item_id__in=selected_ids).delete() # チェックボックスで選択したitemを削除
            
            return redirect("mypage:admin_mypage")
        """
    
    storage_tags = StorageLocationsTag.objects.all()
    order = request.session.get("order", "asc") # セッションから現在のorderを取得。デフォルトは'asc'
    selected_location = request.session.get("selected_location", "")  # セッションから選択された保管場所を取得
    if selected_location == "":
        founditemimages = ItemImage.objects.select_related("item").order_by("item__created_at")
    else:
        founditemimages = ItemImage.objects.select_related("item").order_by("item__created_at")
        location = StorageLocationsTag.objects.get(storage_location_name=selected_location)
        founditemimages = founditemimages.filter(item__storage_location=location)
    if order == "asc":
        founditemimages = founditemimages.order_by("item__created_at")
    elif order == "des":
        founditemimages = founditemimages.order_by("-item__created_at")
    if search_ID == "":
        pass
    else:
        search_ID = int(search_ID) # item_idのデータ型はint
        founditemimages = founditemimages.filter(item__item_id=search_ID)
    print(order)
    print(selected_location)

        # ページネーション処理
    paginator = Paginator(founditemimages, 4)  # 1ページに10件表示
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
       

    return render(request, "administrator.html", {"founditemimages": page_obj, "storagetags": storage_tags})
