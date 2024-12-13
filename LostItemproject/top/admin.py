from django.contrib import admin
from .models import ItemsNameTag, PickedOrDroppedLocationsTag, StorageLocationsTag, Item, ItemImage

class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_display", "created_at")

    def item_display(self, obj):
        return str(obj)

# バックエンド管理への登録モデル
admin.site.register(ItemsNameTag)
admin.site.register(PickedOrDroppedLocationsTag)
admin.site.register(StorageLocationsTag)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage)