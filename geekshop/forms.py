from django import forms

from geekshop.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = ['name', 'description', 'is_active', 'products']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'price', 'quantity', 'image']
