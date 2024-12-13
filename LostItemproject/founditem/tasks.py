# 定时检查数据中可能登记或者时间超时（1个月）


from os.path import basename
import base64
from mimetypes import guess_type
from celery import shared_task
from django.conf import settings
from .models import get_item_model, get_item_image_model, get_items_name_tag_model, \
    get_picked_or_dropped_locations_tag_model, get_storage_locations_tag_model
from utils import email_utils, item_utils
import pprint


@shared_task
def my_scheduled_task():
    print("Executing scheduled task...")
    # 在此处添加您的定时任务逻辑
    return "Task completed!"


@shared_task
def send_periodic_email():
    subject = "定时任务测试邮件"
    message = "这是 Celery 定时任务发送的测试邮件。"
    email_utils.send_email_async(subject=subject,
                                 to_emails=['cralpbin@gmail.com'],
                                 template_name="emails/found_item.html",
                                 context={"item_name": "財布", "found_location": "図書館", "storage_location": "図書館"},
                                 attachments=None)


@shared_task
def match_items_scheduled_task():
    """
        Regular matching items
    """

    item_model = get_item_model()
    itemImage = get_item_image_model()
    itemNameTag = get_items_name_tag_model()
    pickedOrDroppedLocationsTag = get_picked_or_dropped_locations_tag_model()
    storageLocationsTag = get_storage_locations_tag_model()

    # search all of the lost items
    lost_items = item_model.objects.filter(item_type=1)

    for lost_item in lost_items:
        to_email = lost_item.contact_email
        if not to_email:
            print('email of lost_item is null')
            continue

        match_found_items = item_utils.match_found_items(lost_item.item_id)
        if match_found_items and match_found_items != []:

            print("lost item:", lost_item)
            print("deal with lost item :", match_found_items)
            contexts = []
            attachments = []
            for found_item in match_found_items:

                itemName = itemNameTag.objects.get(item_name_id=found_item.item_name_id)
                pickedOrDroppedLocations = pickedOrDroppedLocationsTag.objects.get(
                    PorD_location_id=found_item.PorD_location_id)
                storageLocations = storageLocationsTag.objects.get(
                    storage_location_id=found_item.storage_location_id)

                images = itemImage.objects.filter(item=found_item.item_id)
                base64_images = []  # 用于存储 Base64 编码后的图片信息
                images_urls = []
                if images.exists():
                    for image in images:
                        if image.image_path:
                            with image.image_path.open('rb') as img_file:

                                image_data = img_file.read()
                                # get MIME
                                mime_type, _ = guess_type(image.image_path.name)
                                mime_type = mime_type or "application/octet-stream"  # 默认 MIME 类型
                                print(image.image_path)
                                print(mime_type)

                                base64_str = base64.b64encode(image_data).decode('utf-8')
                                # base64_str = base64_str.replace(" ", "").replace("\n", "").replace("\r", "")
                                # encode image to base64_image
                                base64_image = f"data:{mime_type};base64,{base64_str}"
                                base64_images.append(base64_image)

                                image_url = f"{settings.SITE_DOMAIN}/founditem/image/"+str(image.id)
                                print(image_url)
                                images_urls.append(image_url)

                                attachments.append((basename(image.image_path.name), image_data, mime_type))


                context = {
                    "item_name": str(itemName.item_name),
                    "found_location": str(pickedOrDroppedLocations.picked_or_dropped_location_name),
                    "storage_location": str(storageLocations.storage_location_name),
                    "images": base64_images,
                    "urls": images_urls,
                }

                contexts.append(context)

            email_utils.send_email_async.delay(
                subject="落とし物が見つかるかもしれない",
                to_emails=[to_email],
                template_name="emails/found_item.html",
                context={'found_items': contexts},
                attachments=attachments,
            )
