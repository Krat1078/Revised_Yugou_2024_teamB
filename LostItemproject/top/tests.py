# Create your tests here.
from django.db import transaction
from django.test import TestCase, TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from .models import ItemImage, Item, StorageLocationsTag, ItemsNameTag, PickedOrDroppedLocationsTag
import os


class ImageUploadTestCase(TestCase):
    def setUp(self):
        # 清理媒体目录中的文件，确保每次测试都从干净的状态开始
        media_path = settings.MEDIA_ROOT
        if os.path.exists(media_path):
            for f in os.listdir(media_path):
                file_path = os.path.join(media_path, f)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        else:
            os.makedirs(media_path)

    @transaction.atomic
    def test_image_upload(self):

        with open('E:\Pictures\infinity-4878311.jpg', 'rb') as f:
            image = SimpleUploadedFile(f.name, f.read(), content_type='image/jpeg')
            # 查询item表中的第一条记录
            # item = Item.objects.filter(item_id=2).first()  # Look for item_id = 2
            # 创建标签
        item_name_tag = ItemsNameTag.objects.create(
            item_name="Laptop",
            description="An electronic device used for computing"
        )

        picked_or_dropped_location_tag = PickedOrDroppedLocationsTag.objects.create(
            picked_or_dropped_location_name="Library",
            description="The place where the item was found"
        )

        storage_location_tag = StorageLocationsTag.objects.create(
            storage_location_name="Lost and Found Desk",
            description="The place where lost items are stored"
        )

        # 创建物品
        Item.objects.create(
            item_name=item_name_tag,
            PorD_location=picked_or_dropped_location_tag,
            storage_location=storage_location_tag,
            item_type=0,  # 捡到物品
            status=0,  # 待处理
            contact_email="user@example.com",
            contact_phone="1234567890"
        )
        item = Item.objects.first()
        print(item)
        # 然后插入 item_image 记录
        item_image = ItemImage.objects.create(
            item_id=item.item_id,  # 确保 item_id 已经有对应的 item
            image_path=image,
            uploaded_at="2024-11-20 10:30:00"
        )

        # 确保图片字段已保存
        self.assertTrue(os.path.exists(item_image.image_path.path))


    def tearDown(self):
        # 清理测试后留下的文件
        media_path = settings.MEDIA_ROOT
        if os.path.exists(media_path):
            for f in os.listdir(media_path):
                file_path = os.path.join(media_path, f)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
