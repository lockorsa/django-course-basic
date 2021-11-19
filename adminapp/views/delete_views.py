from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView

from adminapp.views.mixins import AccessMixin, CallableMixin
from authapp.models import ShopUser
from geekshop.models import Category, Product


class UserDelete(CallableMixin, AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/delete_confirm.html'
    success_url = reverse_lazy('adminapp:users')


class CategoryDelete(CallableMixin, AccessMixin, DeleteView):
    model = Category
    template_name = 'adminapp/delete_confirm.html'
    success_url = reverse_lazy('adminapp:categories')


class ProductDelete(CallableMixin, AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/delete_confirm.html'

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
user_delete = UserDelete.as_view()
category_delete = CategoryDelete.as_view()
product_delete = ProductDelete.as_view()
