# Create your tests here.
from django.db import transaction
from django.test import TestCase, TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from .models import ItemImage, Item, StorageLocationsTag, ItemsNameTag, PickedOrDroppedLocationsTag
import os


class ImageUploadTestCase(TestCase):
    def setUp(self):
        # すべてのテストがクリーンな状態から始まるように、メディアディレクトリのファイルをクリーンアップする。
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
            # アイテムテーブルの最初の行を照会する
            # item = Item.objects.filter(item_id=2).first()  # Look for item_id = 2
            # ラベルの作成
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

        # アイテムを作成する
        Item.objects.create(
            item_name=item_name_tag,
            PorD_location=picked_or_dropped_location_tag,
            storage_location=storage_location_tag,
            item_type=0,  # 拾ったもの
            status=0,  # 保留
            contact_email="user@example.com",
            contact_phone="1234567890"
        )
        item = Item.objects.first()
        print(item)
        # 次にitem_imageレコードを挿入する
        item_image = ItemImage.objects.create(
            item_id=item.item_id,  # item_idがすでに対応するアイテムを持っていることを確認する
            image_path=image,
            uploaded_at="2024-11-20 10:30:00"
        )

        # 画像フィールドが保存されていることを確認する
        self.assertTrue(os.path.exists(item_image.image_path.path))


    def tearDown(self):
        # テスト後に残されたファイルのクリーンアップ
        media_path = settings.MEDIA_ROOT
        if os.path.exists(media_path):
            for f in os.listdir(media_path):
                file_path = os.path.join(media_path, f)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
