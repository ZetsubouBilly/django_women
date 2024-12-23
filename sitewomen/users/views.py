from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from sitewomen import settings

from django.contrib.auth import get_user_model

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    # def get_success_url(self) :
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя', 'default_image': settings.DEFAULT_USER_IMAGE,}

    def get_success_url(self) :
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    # extra_context = {'title': 'Профиль пользователя'}
    success_url = reverse_lazy('users:password_change_done')