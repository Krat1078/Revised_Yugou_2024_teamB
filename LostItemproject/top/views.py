from django.shortcuts import render
from .models import ItemImage, ItemsNameTag, PickedOrDroppedLocationsTag, StorageLocationsTag
from .forms import DateFilterForm
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # タグは最初None
    itemname_tag = request.session.get("itemname_tag", None)
    location_tag = request.session.get("location_tag", None)
    storage_tag = request.session.get("storage_tag", None)
    images = ItemImage.objects.select_related("item").order_by("item__created_at") # すべての物品表示（日付順）
    # images = images.filter(item__item_type=0) # item_type = 0の物品だけ表示
    ##########################################################
    ## そもそも画像が登録されるときは必ず「拾得物登録」なので、  
    ## この.filter()はいらない？                             
    #########################################################
    images = images.filter(item__status=0) # status = 0の物品だけ表示
    itemname_tags = ItemsNameTag.objects.all().order_by("item_name")
    location_tags = PickedOrDroppedLocationsTag.objects.all().order_by("picked_or_dropped_location_name")
    storage_tags = StorageLocationsTag.objects.all().order_by("storage_location_name")
    # order = request.session.get("order", "asc") # セッションから現在のorderを取得。デフォルトは'asc'
    date_form = DateFilterForm(request.GET)  # GETでフォームのデータを取得
    if request.method == "POST":
        
        """"""
        date_form = DateFilterForm(request.POST)
        itemname_tag = request.POST.get("item")
        location_tag = request.POST.get("location")
        storage_tag = request.POST.get("storage")
        # セッションに検索条件を保存
        request.session["itemname_tag"] = itemname_tag
        request.session["location_tag"] = location_tag
        request.session["storage_tag"] = storage_tag
        # タグによってフィルタリングをかける 
        if itemname_tag and location_tag and storage_tag:
            images = images.filter(Q(item__item_name=itemname_tag) & Q(item__PorD_location=location_tag) & Q(item__storage_location=storage_tag))
        elif itemname_tag and location_tag:
            images = images.filter(Q(item__item_name=itemname_tag) & Q(item__PorD_location=location_tag))
        elif itemname_tag and storage_tag:
            images = images.filter(Q(item__item_name=itemname_tag) & Q(item__storage_location=storage_tag))
        elif location_tag and storage_tag:
            images = images.filter(Q(item__PorD_location=location_tag) & Q(item__storage_location=storage_tag))
        elif itemname_tag:
            images = images.filter(item__item_name=itemname_tag)
        elif location_tag:
            images = images.filter(item__PorD_location=location_tag)
        elif storage_tag:
            images = images.filter(item__storage_location=storage_tag)
        # ItemImageモデルのインスタンスを取得し、その関連するItemとItemNameTagを一度に取得
        if date_form.is_valid():
            date = date_form.cleaned_data.get("date")
            if date:
                images = images.filter(item__created_at__gte=date)
        """
        if request.POST.get("action") == "change_order":
            if order == "asc":
                images = images.order_by("-item__created_at")
                next_order = "des"
                print(order)
            elif order == "des":
                images = images.order_by("item__created_at")
                next_order = "asc"
                print(order)
            request.session['order'] = next_order
        """
    
    # ページネーションの設定
    paginator = Paginator(images, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        #"images": images, 
        "images": page_obj,
        # "form": form, 
        "date_form": date_form,
        "page_obj": page_obj,
        "itemnametags": itemname_tags,
        "locationtags": location_tags,
        "storagetags": storage_tags,
    }

    return render(request, 'index.html', context)
