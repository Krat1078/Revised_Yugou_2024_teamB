from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.apps import apps

from .forms import (
    UserRegisterForm,
)

# Create your views here.
from django.views.generic import CreateView


def index(request):
    return render(request, 'lostitem_index.html')


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        # 判断用户是否为管理员
        if self.request.user.is_superuser:
            # 如果是管理员，跳转到 Django 后台管理页面
            return reverse_lazy('admin:index')
        else:
            # 如果是普通用户，跳转到主页
            return reverse_lazy('top:home')  # 假设主页的 URL 名称是 'home'


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

    # for LocationsTag in LocationsTags:
    #     print(LocationsTag.storage_location_id)

    # back to html
    return render(request, 'items/lost_item_register.html', {
        'locations': LocationsTags,
        'categories': itemsNameTags
    })


# click register items to save it
def register_item(request):
    if request.method == 'POST':
        Item = apps.get_model('top', 'Item')
        ItemImage = apps.get_model('top', 'ItemImage')

        # item = Item.objects.create(
        #     name=request.POST.get('name'),
        #     description=request.POST.get('description')
        # )

        post_data = request.POST
        color = post_data.get('color')
        location = post_data.get('location')
        category = post_data.get('category')
        print(post_data)
        # 记录这里图片取不到，可以考虑图片单独上传
        for file in request.FILES.getlist('images'):
            # ItemImage.objects.create(item=item, image=file)
            print(file)

        return HttpResponse(f"Location: {location}, Category: {category}, Color: {color}")
    return HttpResponse("Please submit the form.")
