from django.apps import apps


def get_picked_or_dropped_locations_tag_model():
    return apps.get_model('top', 'PickedOrDroppedLocationsTag')


def get_items_name_tag_model():
    return apps.get_model('top', 'ItemsNameTag')


def get_storage_locations_tag_model():
    return apps.get_model('top', 'StorageLocationsTag')


def get_item_model():
    return apps.get_model('top', 'Item')


def get_item_image_model():
    return apps.get_model('top', 'ItemImage')
