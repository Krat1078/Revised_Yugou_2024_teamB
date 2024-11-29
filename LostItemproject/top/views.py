from django.shortcuts import render
from .models import ItemImage

# Create your views here.
def index(request):
    # ItemImageモデルのインスタンスを取得し、その関連するItemとItemNameTagを一度に取得
    images = ItemImage.objects.select_related("item__item_name").all()
    return render(request, 'index.html', {"images": images})
