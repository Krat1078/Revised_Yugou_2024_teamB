from django.db.models import Q
from top.models import Item  # 替换为你的实际模型路径


def match_items(found_item_ids):
    """
    匹配找到物品的相似物品。

    :param found_item_ids: 找到物品的ID列表（可以是单个ID）
    :return: 匹配的物品列表
    """
    if not found_item_ids:
        print("found_item_ids is None")
        return []

    # 如果传入的是单个 ID，将其包装成列表
    if isinstance(found_item_ids, int):
        found_item_ids = [found_item_ids]

    matched_items = []

    # 遍历找到物品的 ID 列表
    for item_id in found_item_ids:

        try:
            # 查询找到的物品对象
            found_item = Item.objects.get(item_id=item_id, item_type=0)
        except Item.DoesNotExist:
            continue

        # 构建查询条件，排除找到的物品本身
        query = Q(item_type=1)  # 匹配 item_type 为 1 的物品
        if found_item.item_name:
            query &= Q(item_name=found_item.item_name)
        if found_item.PorD_location:
            query &= Q(PorD_location=found_item.PorD_location)
        query &= (Q(status=0) | Q(status=1))

        # 查询数据库，找到匹配的物品
        similar_items = Item.objects.filter(query).exclude(item_id=item_id)

        # 将查询结果添加到返回列表中
        matched_items.extend(similar_items)

    return matched_items
