from PIL import Image, UnidentifiedImageError
import hashlib
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from utils import email_utils, item_utils

from . import models


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
                    # 检查尺寸
                    width, height = img.size
                    if width > 1920 or height > 1080:
                        errors.append(f"{image.name} exceeds maximum dimensions (1920x1080).")

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
        )

        # save image
        for file in images:
            itemImage.objects.create(item_id=item.item_id, image_path=file, uploaded_at=timezone.now())

        match_lost_items = item_utils.match_items(item.item_id)

        if match_lost_items:
            attachments = []
            if images:
                for image in images:
                    image.seek(0)
                    image_data = image.read()
                    attachments.append((image.name, image_data, "image/jpeg"))

            for lost_item in match_lost_items:
                email = lost_item.contact_email
                if email:
                    itemName = itemNameTag.objects.get(item_name_id=lost_item.item_name_id)
                    pickedOrDroppedLocations = pickedOrDroppedLocationsTag.objects.get(
                        PorD_location_id=lost_item.PorD_location_id)
                    storageLocations = storageLocationsTag.objects.get(
                        storage_location_id=lost_item.storage_location_id)

                    # Calling Celery asynchronous tasks
                    email_utils.send_email_async.delay(
                        subject="落とし物が見つかるかもしれない",
                        to_emails=[email],
                        template_name="emails/found_item.html",
                        context={
                            "item_name": str(itemName.item_name),
                            "found_location": str(pickedOrDroppedLocations.picked_or_dropped_location_name),
                            "storage_location": str(storageLocations.storage_location_name),
                        },
                        attachments=attachments
                    )

        return JsonResponse({'status': 'success', 'message': 'Item registered successfully.'})

    return HttpResponse("Please submit the form.", status=405)
