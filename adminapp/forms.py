from django import forms
from django.contrib.auth.forms import UserCreationForm

from authapp.forms import ShopUserEditForm, ShopUserRegisterForm
from authapp.models import ShopUser
from geekshop.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active', 'products']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'price', 'quantity', 'image']


class UserEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class UserCreateForm(ShopUserRegisterForm):
    pass
