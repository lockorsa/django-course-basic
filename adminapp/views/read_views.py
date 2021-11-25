from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from adminapp.views.mixins import AccessMixin, CallableMixin
from authapp.models import ShopUser
from geekshop.models import Category, Product


class Admin(CallableMixin, AccessMixin, TemplateView):
    template_name = 'adminapp/admin.html'


class UserList(CallableMixin, AccessMixin, ListView):
    model = ShopUser
    ordering = ['-is_active']
    template_name = 'adminapp/users.html'


class CategoryList(CallableMixin, AccessMixin, ListView):
    model = Category
    ordering = ['-is_active']
    template_name = 'adminapp/categories.html'


class ProductList(CallableMixin, AccessMixin, ListView):
    model = Product
    ordering = ['-is_active']
    template_name = 'adminapp/products.html'

    def get_queryset(self, *args, **kwargs):
        """Фильтруем продукты по принадлежности к выбранной категории"""
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(categories__pk=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        """Добавляем в контекст необходимый объект категории."""
        context = super().get_context_data(*args, **kwargs)
        context['category'] = get_object_or_404(
            Category,
            pk=self.kwargs.get('pk'),
        )
        return context


class ProductDetail(CallableMixin, AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст категорию товара."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            pk=self.object.categories.first().pk,
        )
        return context


# алиасы
admin = Admin.as_view()
users = UserList.as_view()
categories = CategoryList.as_view()
products = ProductList.as_view()
product_detail = ProductDetail.as_view()
