from django.shortcuts import render
from .models import Item
from .models import ItemImage
from django.apps import apps
from django.conf import settings


# Create your views here.
def index(request):
    items=Item.objects.order_by("-created_at")
    itemimages=ItemImage.objects.order_by("-uploaded_at")
  
    
    return render(request,"index_sample.html",{"itemimages":itemimages})


    
