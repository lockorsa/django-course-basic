from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from adminapp.forms import CategoryForm, ProductForm, UserEditForm
from adminapp.views.mixins import AccessMixin, CallableMixin
from authapp.models import ShopUser
from geekshop.models import Category, Product


class UserUpdate(CallableMixin, AccessMixin, UpdateView):
    model = ShopUser
    form_class = UserEditForm
    template_name = 'adminapp/form.html'
    success_url = reverse_lazy('adminapp:users')


class CategoryUpdate(CallableMixin, AccessMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'adminapp/form.html'
    success_url = reverse_lazy('adminapp:categories')


class ProductUpdate(CallableMixin, AccessMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'adminapp/form.html'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст необходимый объект категории."""
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['category'] = get_object_or_404(
            Category,
            pk=self.object.categories.first().pk,
        )
        return context

    def get_success_url(self):
        context = self.get_context_data()
        category = context.get('category')
        return reverse('adminapp:products', kwargs={
            'pk': category.pk,
        })


# алиасы
user_update = UserUpdate.as_view()
category_update = CategoryUpdate.as_view()
product_update = ProductUpdate.as_view()
