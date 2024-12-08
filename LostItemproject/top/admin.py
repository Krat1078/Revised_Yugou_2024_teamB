from django.contrib import admin
from .models import ItemsNameTag, PickedOrDroppedLocationsTag, StorageLocationsTag, Item, ItemImage

# バックエンド管理への登録モデル
admin.site.register(ItemsNameTag)
admin.site.register(PickedOrDroppedLocationsTag)
admin.site.register(StorageLocationsTag)
admin.site.register(Item)
admin.site.register(ItemImage)