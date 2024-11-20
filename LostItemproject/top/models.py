from django.db import models


class ItemsNameTag(models.Model):
    item_name_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100, verbose_name="Name tags for items",
                                 help_text="Stationery, clothing, electronic equipment, etc.")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.item_name


class PickedOrDroppedLocationsTag(models.Model):
    PorD_location_id = models.AutoField(primary_key=True)
    picked_or_dropped_location_name = models.CharField(max_length=100, verbose_name="Location Name",
                                                       help_text="Name of the place where it was found or dropped, e.g., faculty building, student center, etc.")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.picked_or_dropped_location_name


class StorageLocationsTag(models.Model):
    storage_location_id = models.AutoField(primary_key=True)
    storage_location_name = models.CharField(max_length=100, verbose_name="Storage Location Name",
                                             help_text="Name of the place to store lost items, e.g., administrative office, library, etc.")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.storage_location_name


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.ForeignKey(ItemsNameTag, on_delete=models.CASCADE, verbose_name="Item Name")
    PorD_location = models.ForeignKey(PickedOrDroppedLocationsTag, on_delete=models.CASCADE,
                                      verbose_name="Picked or Dropped Location")
    storage_location = models.ForeignKey(StorageLocationsTag, on_delete=models.CASCADE, verbose_name="Storage Location")
    item_type = models.IntegerField(verbose_name="Item Type", help_text="0: Found, 1: Lost")
    status = models.SmallIntegerField(verbose_name="Status", help_text="0: Pending, 1: In Progress, 2: Resolved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    contact_email = models.EmailField(max_length=100, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Item {self.item_id}: {self.item_name}"


class ItemImage(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    image_path = models.CharField(max_length=225, verbose_name="Image Path")
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Image for Item {self.item.item_id}"
