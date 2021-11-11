from django.shortcuts import render

from authapp.models import ShopUser
from geekshop.models import Category, Product


def admin(request):
    return render(request, 'adminapp/admin.html')


def users(request):
    pass


def user_create(request):
    pass


def user_update(request, pk: int):
    pass


def user_delete(request, pk: int):
    pass


def categories(request):
    pass


def category_create(request):
    pass


def category_update(request, pk: int):
    pass


def category_delete(request, pk: int):
    pass


def products(request):
    pass


def product_create(request):
    pass


def product_update(request, pk: int):
    pass


def product_delete(request, pk: int):
    pass


def product_datail(request, pk: int):
    pass
