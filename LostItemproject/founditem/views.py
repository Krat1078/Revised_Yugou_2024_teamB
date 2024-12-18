from PIL import Image, UnidentifiedImageError
import hashlib
from datetime import datetime
import json

from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from utils import email_utils, item_utils, QR_utils

from . import models

@csrf_exempt
def validate_qr_code(request):
    if request.method == "POST":
        try:
            qr_data = request.POST.get("qr_code") or json.loads(request.body).get("qr_code")
            try:
                # 如果 qr_data 是字符串，尝试解析
                if isinstance(qr_data, str):
                    # 将单引号替换为双引号，转换为标准 JSON 格式
                    if qr_data.startswith("{") and qr_data.endswith("}"):
                        qr_data = qr_data.replace("'", '"')  # 替换单引号为双引号
                    qr_code = json.loads(qr_data)  # 尝试解析为字典
                else:
                    qr_code = qr_data  # 已经是字典，直接使用
            except json.JSONDecodeError as e:
                return JsonResponse({"status": "error", "message": ""})

            # 解析 QR 数据并验证时限
            valid, message = QR_utils.validate_qr_code(qr_code)  # 自定义验证逻辑
            if valid:
                return JsonResponse({"status": "success", "message": "QRコードが有効です。"})
            else:
                return JsonResponse({"status": "error", "message": message})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

# Create your views here.
def index(request):
    return render(request, 'founditem_index.html')


# from home page to lostitemregister
def tofounditemregister(request):
    # search from database
    # from top app get models
    storageLocationsTag = models.get_storage_locations_tag_model()
    itemsNameTag = models.get_items_name_tag_model()
    pickedOrDroppedLocationsTag = models.get_picked_or_dropped_locations_tag_model()
    # do search
    LocationsTags = storageLocationsTag.objects.all()
    itemsNameTags = itemsNameTag.objects.all()
    pickedOrDroppedLocationsTags = pickedOrDroppedLocationsTag.objects.all()

    # back to html
    return render(request, 'items/found_item_register.html', {
        'locations': LocationsTags,
        'pickedOrDroppedLocationsTags': pickedOrDroppedLocationsTags,
        'categories': itemsNameTags,
    })


# click register items to save it
def register_item(request):
    if request.method == 'POST':

        # get data from post
        post_data = request.POST
        data = post_data.get('data')
        location = post_data.getlist('location')
        category = post_data.get('category')
        color = post_data.get('color')
        description = post_data.get('comment')
        errors = []
        data = parse_date(data)
        if not data:
            errors.append("error': 'Invalid date format")
        data = timezone.make_aware(datetime.combine(data, datetime.min.time()))
        if not category:
            errors.append("item category is required.")
        if not location:
            errors.append("Location is required.")
        if not category:
            errors.append("Category is required.")
        if description and len(description) > 500:
            errors.append("Description length must not exceed 500 characters.")

        images = request.FILES.getlist('images')
        # Used to store the hash value of the image and check for duplication
        image_hashes = set()
        for image in images:
            try:
                img = Image.open(image)
                img_format = img.format.lower()
                if img_format not in ['jpg', 'jpeg', 'png', 'gif']:
                    errors.append(f'{image.name} is not a valid image format (JPG, JPEG, PNG, GIF only).')
                else:
                    # 检查重复
                    image.seek(0)
                    image_hash = hashlib.md5(image.read()).hexdigest()
                    if image_hash in image_hashes:
                        errors.append(f"Duplicate image detected: {image.name}")
                    else:
                        image_hashes.add(image_hash)
                image.seek(0)
            except UnidentifiedImageError:
                errors.append(f'{image.name} is not a valid image format.')

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        item = models.get_item_model()
        itemImage = models.get_item_image_model()
        itemNameTag = models.get_items_name_tag_model()
        pickedOrDroppedLocationsTag = models.get_picked_or_dropped_locations_tag_model()
        storageLocationsTag = models.get_storage_locations_tag_model()

        # save to item
        item = item.objects.create(
            item_name=get_object_or_404(itemNameTag, pk=category),
            PorD_location=get_object_or_404(pickedOrDroppedLocationsTag, pk=location[0]),
            storage_location=get_object_or_404(storageLocationsTag, pk=location[1]),
            item_type=0,
            status=0,
            created_at=data,
            updated_at=timezone.now(),
            contact_email='',
            contact_phone=post_data.get('contact_phone'),
            description=description,
        )

        # save image
        for file in images:
            itemImage.objects.create(item_id=item.item_id, image_path=file, uploaded_at=timezone.now())

        # match_lost_items = item_utils.match_items(item.item_id)
        #
        # if match_lost_items:
        #     attachments = []
        #     if images:
        #         for image in images:
        #             image.seek(0)
        #             image_data = image.read()
        #             attachments.append((image.name, image_data, "image/jpeg"))
        #
        #     for lost_item in match_lost_items:
        #         email = lost_item.contact_email
        #         if email:
        #             itemName = itemNameTag.objects.get(item_name_id=lost_item.item_name_id)
        #             pickedOrDroppedLocations = pickedOrDroppedLocationsTag.objects.get(
        #                 PorD_location_id=lost_item.PorD_location_id)
        #             storageLocations = storageLocationsTag.objects.get(
        #                 storage_location_id=lost_item.storage_location_id)
        #
        #             # Calling Celery asynchronous tasks
        #             email_utils.send_email_async.delay(
        #                 subject="落とし物が見つかるかもしれない",
        #                 to_emails=[email],
        #                 template_name="emails/found_item.html",
        #                 context={
        #                     "item_name": str(itemName.item_name),
        #                     "found_location": str(pickedOrDroppedLocations.picked_or_dropped_location_name),
        #                     "storage_location": str(storageLocations.storage_location_name),
        #                 },
        #                 attachments=attachments
        #             )

        return JsonResponse({'status': 'success', 'message': 'Item registered successfully.'})

    return HttpResponse("Please submit the form.", status=405)


def get_image(request, id):
    ItemImage = models.get_item_image_model()
    try:
        # 获取对应的 ItemImage 对象
        item_image = get_object_or_404(ItemImage, id=id)

        # 获取图片的实际路径
        image_path = item_image.image_path.path  # 假设图片保存在 MEDIA_URL 目录下
        # 打开并返回图片文件
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')

    except ItemImage.DoesNotExist:
        # 如果找不到对应的 ItemImage，则返回错误信息
        errors = ["Item image not found."]
        return JsonResponse({'status': 'error', 'errors': errors}, status=404)

    except Exception as e:
        # 捕获其他异常并返回错误信息
        errors = [str(e)]  # 捕获并返回异常信息
        return JsonResponse({'status': 'error', 'errors': errors}, status=400)
