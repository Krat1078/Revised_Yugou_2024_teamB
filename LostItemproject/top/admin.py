from django.contrib import admin
from .models import ItemsNameTag, PickedOrDroppedLocationsTag, StorageLocationsTag, Item, ItemImage

# バックエンド管理への登録モデル
admin.site.register(ItemsNameTag)
admin.site.register(PickedOrDroppedLocationsTag)
admin.site.register(StorageLocationsTag)
# admin.site.register(Item)
admin.site.register(ItemImage)


class ItemAdmin(admin.ModelAdmin):
    # 自定义展示的字段
    list_display = ('item_id', 'item_name', 'PorD_location', 'storage_location', 'item_type', 'contact_email')
    # 添加可搜索字段
    search_fields = ('item_name', 'PorD_location', 'contact_email')
    # 添加过滤器
    list_filter = ('created_at',)
    # 设置每页显示条目数
    list_per_page = 20

    # 自定义字段方法
    @admin.display(description='Summary')
    def summary(self, obj):
        return f"{obj.description[:50]}..." if obj.description else "No Description"


# 注册模型和对应的 Admin 配置
admin.site.register(Item, ItemAdmin)
