from django.shortcuts import render
from .models import ItemImage
from .forms import TagFilterForm, DateFilterForm
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # タグは最初None
    itemname_tag = None
    location_tag = None
    images = ItemImage.objects.select_related("item__item_name").all() # すべての物品表示
    # images = images.filter(item__item_type=0) # item_type = 0の物品だけ表示
    ##########################################################
    ## そもそも画像が登録されるときは必ず「拾得物登録」なので、  
    ## この.filter()はいらない？                             
    #########################################################
    images = images.filter(item__status=0) # status = 0の物品だけ表示
    if request.method == "POST":
        form = TagFilterForm(request.POST) # form.pyからimport
        date_form = DateFilterForm(request.POST)
        if form.is_valid():
            # python側の変数にタグ情報を格納する
            itemname_tag = form.cleaned_data['itemname_tag']
            location_tag = form.cleaned_data["location_tag"]
            # タグによってフィルタリングをかける 
            if itemname_tag and location_tag:
                images = images.filter(Q(item__item_name=itemname_tag) & Q(item__PorD_location=location_tag))
            elif itemname_tag:
                images = images.filter(item__item_name=itemname_tag)
            elif location_tag:
                images = images.filter(item__PorD_location=location_tag)
            # ItemImageモデルのインスタンスを取得し、その関連するItemとItemNameTagを一度に取得
        if date_form.is_valid():
            date = date_form.cleaned_data.get("date")
            if date:
                images = images.filter(item__created_at__gte=date)   
        
    else:
        form = TagFilterForm()
        date_form = DateFilterForm()
    
    # ページネーションの設定
    paginator = Paginator(images, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        #"images": images, 
        "images": page_obj,
        "form": form, 
        "date_form": date_form,
        "page_obj": page_obj,
    }

    return render(request, 'index.html', context)
