from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from authapp.forms import (
    ShopUserEditForm, ShopUserLoginForm, ShopUserRegisterForm,
)
from authapp.models import ShopUser


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            # здесь вернется bool-флаг отправки, можно обработать
            send_verification_email(user)
            return HttpResponseRedirect(reverse('index:index'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context=context)


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)

    next_param = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponseRedirect(reverse('index:index'))

    context = {
        'login_form': login_form,
        'next': next_param,
    }
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index:index'))


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'authapp/edit.html', context=context)


def verify(request, email, key):
    user = get_object_or_404(
        ShopUser,
        email=email,
        register_activation_key=key,
    )
    if not user.is_activation_key_expired():
        user.activate()
        auth.login(request, user)
        return render(request, 'authapp/activation_success.html')
    return HttpResponseBadRequest('ошибка')


def send_verification_email(user):
    verification_link = reverse('authapp:verify', args=[
        user.email,
        user.register_activation_key,
    ])
    full_link = settings.BASE_URL + verification_link
    # так линтер не ругается на форматирование)
    message = 'Your activation link: {link}'.format(link=full_link)

    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
