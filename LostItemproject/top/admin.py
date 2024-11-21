from django.contrib import admin
from .models import ItemsNameTag, PickedOrDroppedLocationsTag, StorageLocationsTag, Item, ItemImage

# 注册模型到后台管理
admin.site.register(ItemsNameTag)
admin.site.register(PickedOrDroppedLocationsTag)
admin.site.register(StorageLocationsTag)
admin.site.register(Item)
admin.site.register(ItemImage)