from django.db.models import Q
from top.models import Item


def match_items(found_item_ids):
    """
    類似したアイテムと見つかったアイテムを照合します。

    :param found_item_ids: 見つかったアイテムの ID のリスト (単一 ID も可能)
    :return: 一致する項目のリスト
    """
    if not found_item_ids:
        print("found_item_ids is None")
        return []

    # 単一の ID が渡された場合は、それをリストにラップします
    if isinstance(found_item_ids, int):
        found_item_ids = [found_item_ids]

    matched_items = []

    # 見つかったアイテムの ID リストを反復処理します
    for item_id in found_item_ids:

        try:
            found_item = Item.objects.get(item_id=item_id, item_type=0)
        except Item.DoesNotExist:
            continue

        query = Q(item_type=1)
        if found_item.item_name:
            query &= Q(item_name=found_item.item_name)
        if found_item.PorD_location:
            query &= Q(PorD_location=found_item.PorD_location)
        query &= (Q(status=0) | Q(status=1))

        similar_items = Item.objects.filter(query).exclude(item_id=item_id)

        matched_items.extend(similar_items)

    return matched_items
