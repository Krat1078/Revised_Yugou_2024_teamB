from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

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
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    success_message = "Now you are registered, try to log in!"
