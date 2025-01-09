import imghdr
import os.path

from PIL import Image, UnidentifiedImageError
import hashlib
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.apps import apps
from django.core.files.images import get_image_dimensions
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages

from .forms import (
    UserRegisterForm,
    UserRegistrationForm,
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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 用户暂时不可用，等待激活 # ユーザーは一時的に利用できません。
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 发送激活邮件 # アクティベーションメールを送信する
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            # print(urlsafe_base64_encode(force_bytes(user.pk)))
            send_mail(subject, message, '1528392308@qq.com', [user.email])

            return render(request, 'email/check_email.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


# activate user
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('lostitem:login')  # redirect to 'login'
    else:
        return HttpResponse('Activation link is invalid!')


# from home page to lostitemregiste
def tolostitemregister(request):
    # search from database
    # from top app get models
    storageLocationsTag = apps.get_model('top', 'StorageLocationsTag')
    pickedOrDroppedLocationsTag = apps.get_model("top", "PickedOrDroppedLocationsTag")
    itemsNameTag = apps.get_model('top', 'ItemsNameTag')
    # do search
    LocationsTags = storageLocationsTag.objects.all()
    PorDLocationsTags = pickedOrDroppedLocationsTag.objects.all()
    itemsNameTags = itemsNameTag.objects.all()

    # back to html
    return render(request, 'items/lost_item_register.html', {
        'locations': PorDLocationsTags,
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

        """Maybe I don't need this place. (Lost and found registration does not require image registration.)
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
        """

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        item = apps.get_model('top', 'Item')
        ##### Maybe I don't need this place. (Lost and found registration does not require image registration.)
        # itemImage = apps.get_model('top', 'ItemImage')

        # save to item
        item = item.objects.create(
            item_name=get_object_or_404(apps.get_model('top', 'ItemsNameTag'), pk=category),
            PorD_location=get_object_or_404(apps.get_model('top', 'PickedOrDroppedLocationsTag'), pk=location),
            storage_location=None,
            # storage_location=get_object_or_404(apps.get_model('top', 'StorageLocationsTag'), pk=location),
            item_type=1,
            status=0,
            created_at=data,
            updated_at=timezone.now(),
            contact_email=user_email,
            contact_phone=post_data.get('contact_phone'),
            description=description,
        )

        #### Maybe I don't need this place. (Lost and found registration does not require image registration.)
        # save image
        # for file in images:
        #   itemImage.objects.create(item_id=item.item_id, image_path=file, uploaded_at=timezone.now())

        return JsonResponse({'status': 'success', 'message': 'Item registered successfully.'})

    return HttpResponse("Please submit the form.", status=405)
