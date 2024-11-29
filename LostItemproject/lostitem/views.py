import imghdr
import hashlib

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.apps import apps
from django.core.files.images import get_image_dimensions
from django.utils import timezone

from .forms import (
    UserRegisterForm,
)

# Create your views here.
from django.views.generic import CreateView


def index(request):
    return render(request, 'lostitem_index.html')


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')
        else:
            return reverse_lazy('top:home')


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('lostitem:login')
    template_name = 'users/signup.html'
    success_message = "Now you are registered, try to log in!"


# from home page to lostitemregiste
def tolostitemregister(request):
    # search from database
    # from top app get models
    storageLocationsTag = apps.get_model('top', 'StorageLocationsTag')
    itemsNameTag = apps.get_model('top', 'ItemsNameTag')
    # do search
    LocationsTags = storageLocationsTag.objects.all()
    itemsNameTags = itemsNameTag.objects.all()

    # back to html
    return render(request, 'items/lost_item_register.html', {
        'locations': LocationsTags,
        'categories': itemsNameTags
    })


# click register items to save it
@login_required
def register_item(request):
    if request.method == 'POST':
        # 获取当前登录用户的 email
        user_email = request.user.email
        if not user_email:
            return JsonResponse({'status': 'error', 'errors': ['User email is not available.']}, status=400)

        # get data from post
        post_data = request.POST
        data = post_data.get('data')
        location = post_data.get('location')
        category = post_data.get('category')
        color = post_data.get('color')
        description = post_data.get('comment')
        print(post_data)

        errors = []
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
            # check image is '.jpg'...
            if imghdr.what(image) not in ['jpeg', 'png', 'gif']:
                errors.append(f'{image.name} is not a valid image format (JPEG, PNG, GIF only).')
            else:
                # check size of image
                width, height = get_image_dimensions(image)
                if width > 1920 or height > 1080:
                    errors.append(f"{image.name} exceeds maximum dimensions (1920x1080).")

            # Calculate the hash value of the image and check whether it is repeated
            image.seek(0)
            image_hash = hashlib.md5(image.read()).hexdigest()
            if image_hash in image_hashes:
                errors.append(f"Duplicate image detected: {image.name}")
            else:
                image_hashes.add(image)
            image.seek(0)

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        item = apps.get_model('top', 'Item')
        itemImage = apps.get_model('top', 'ItemImage')

        # save to item
        item = item.objects.create(
            item_name=get_object_or_404(apps.get_model('top', 'ItemsNameTag'), pk=category),
            PorD_location=get_object_or_404(apps.get_model('top', 'PickedOrDroppedLocationsTag'), pk=location),
            storage_location=get_object_or_404(apps.get_model('top', 'StorageLocationsTag'), pk=location),
            item_type=1,
            status=0,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            contact_email=user_email,
            contact_phone=post_data.get('contact_phone'),
        )

        # save image
        for file in images:
            itemImage.objects.create(item_id=item.item_id, image_path=file, uploaded_at=timezone.now())

        return JsonResponse({'status': 'success', 'message': 'Item registered successfully.'})

    return HttpResponse("Please submit the form.", status=405)
