from django.shortcuts import render, get_object_or_404, redirect
from top.models import Item, ItemImage, StorageLocationsTag
from django.core.paginator import Paginator

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

"""
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

def admin_mypage(request):
    search_ID = ""
    
    if request.method == "POST":
        action = request.POST.get("action")
        selected_ids = request.POST.getlist("selected_items")
        
        if action == "search":
            search_ID = request.POST.get("IDsearch")
        elif action == "delete":
            if selected_ids:
                Item.objects.filter(item_id__in=selected_ids).delete()
            return redirect("mypage:admin_mypage")
        elif action == "search_location":
            request.session["selected_location"] = request.POST.get("search_location")
        elif action == "change_location":
            if request.POST.get("before_location"):
                before_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("before_location"))
                after_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("after_location"))
                change_items = ItemImage.objects.filter(item__storage_location=before_location)
                for change_item in change_items:
                    change_item.item.storage_location = after_location
                    change_item.item.save()
                return redirect("mypage:admin_mypage")
        elif action == "change_order":
            order = request.session.get("order", "asc")
            request.session['order'] = "des" if order == "asc" else "asc"
    
    storage_tags = StorageLocationsTag.objects.all()
    order = request.session.get("order", "asc")
    selected_location = request.session.get("selected_location", "")
    founditemimages = ItemImage.objects.select_related("item").order_by("item__created_at")
    
    if selected_location:
        location = StorageLocationsTag.objects.get(storage_location_name=selected_location)
        founditemimages = founditemimages.filter(item__storage_location=location)
    if order == "des":
        founditemimages = founditemimages.order_by("-item__created_at")
    if search_ID:
        founditemimages = founditemimages.filter(item__item_id=int(search_ID))

     # ページネーション処理
    paginator = Paginator(founditemimages, 10)  # 1ページに10件表示
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "administrator.html", {
        "founditemimages": page_obj,
        "storagetags": storage_tags,
        "selected_location": selected_location,
        "order": order,
        "search_ID": search_ID
    })
"""


def admin_mypage(request): 

     # username = request.user # ユーザー名の取得
        # founditems = Item.objects.filter(item_type=0).order_by("created_at") 
        #founditemimages = founditemimages.filter(item__status=0) # status = 0の物品だけ表示
        # founditem_ids = founditemimages.values_list("item__item_id", flat=True) # 拾得物のID取得

    search_ID = ""

    if request.method == "POST":

        action = request.POST.get("action") # 機能によってPOSTリクエストの遷移を変えるためのaction
        selected_ids = request.POST.getlist("selected_items") # チェックボックスで選択されたitem一覧
        #request.session["selected_location"] = request.POST.get("search_location")  # 保管場所をセッションに保存

        if action == "search": # ID検索機能
            search_ID = request.POST.get("IDsearch")

        elif action == "delete": # データ削除機能
            print(request.__dict__)
            if len(selected_ids) == 0:
                pass
            else:
                Item.objects.filter(item_id__in=selected_ids).delete() # チェックボックスで選択したitemを削除
            
            return redirect("mypage:admin_mypage")
        
        elif action == "search_location":
            request.session["selected_location"] = request.POST.get("search_location")  # 保管場所をセッションに保存
        
        elif action == "change_location": # 保管場所変更機能
            if request.POST.get("before_location") == "":
                pass
            else:
                before_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("before_location"))
                after_location = StorageLocationsTag.objects.get(storage_location_name=request.POST.get("after_location"))
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
    paginator = Paginator(founditemimages, 20)  # 1ページに10件表示
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
       

    return render(request, "administrator.html", {"founditemimages": page_obj, "storagetags": storage_tags})
