from django.shortcuts import render
from .models import ItemImage, ItemsNameTag, PickedOrDroppedLocationsTag, StorageLocationsTag
from .forms import DateFilterForm
from django.db.models import Q
from django.core.paginator import Paginator
import datetime

# Create your views here.
def index(request):

    date_form = DateFilterForm(request.GET)
    date = None
    if date_form.is_valid():
        date = date_form.cleaned_data.get("date")

    itemname_tag = request.GET.get("item", "")
    location_tag = request.GET.get("location", "")
    storage_tag = request.GET.get("storage", "")
    page_number = request.GET.get("page", 1)  # ページ番号もGETで取得
    
    images = ItemImage.objects.select_related("item").order_by("item__created_at")  # すべての物品表示（日付順）

    if itemname_tag:
        images = images.filter(item__item_name__item_name=itemname_tag)
    if location_tag:
        images = images.filter(item__PorD_location__picked_or_dropped_location_name=location_tag)
    if storage_tag:
        images = images.filter(item__storage_location__storage_location_name=storage_tag)
    if date:
        images = images.filter(item__created_at__gte=date)

    # ページネーション
    paginator = Paginator(images, 8)
    page_obj = paginator.get_page(page_number)

    itemname_tags = ItemsNameTag.objects.all().order_by("item_name")
    location_tags = PickedOrDroppedLocationsTag.objects.all().order_by("picked_or_dropped_location_name")
    storage_tags = StorageLocationsTag.objects.all().order_by("storage_location_name")

    context = {
        "images": page_obj,
        "date_form": date_form,
        "page_obj": page_obj,
        "itemnametags": itemname_tags,
        "locationtags": location_tags,
        "storagetags": storage_tags,
        "itemname_tag": itemname_tag,
        "location_tag": location_tag,
        "storage_tag": storage_tag,
    }

    return render(request, 'index.html', context)