from django.db.models import Q
from top.models import Item


def match_lost_items(found_item_ids):
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



def match_found_items(lost_item_ids):
    """
    類似したアイテムと見つかったアイテムを照合します。

    :param found_item_ids: 見つかったアイテムの ID のリスト (単一 ID も可能)
    :return: 一致する項目のリスト
    """
    if not lost_item_ids:
        print("lost_item_ids is None")
        return []

    # 単一の ID が渡された場合は、それをリストにラップします
    if isinstance(lost_item_ids, int):
        lost_item_ids = [lost_item_ids]

    matched_items = []

    # 見つかったアイテムの ID リストを反復処理します
    for item_id in lost_item_ids:

        try:
            lost_item = Item.objects.get(item_id=item_id, item_type=1)
        except Item.DoesNotExist:
            continue

        query = Q(item_type=0)
        if lost_item.item_name:
            query &= Q(item_name=lost_item.item_name)
        if lost_item.PorD_location:
            query &= Q(PorD_location=lost_item.PorD_location)
        query &= (Q(status=0) | Q(status=1))

        similar_items = Item.objects.filter(query).exclude(item_id=item_id)

        matched_items.extend(similar_items)

    return matched_items
