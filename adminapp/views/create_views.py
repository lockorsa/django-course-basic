from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from adminapp.forms import CategoryForm, ProductForm, UserCreateForm
from adminapp.views.mixins import AccessMixin, CallableMixin
from authapp.models import ShopUser
from geekshop.models import Category, Product


class UserCreate(CallableMixin, AccessMixin, CreateView):
    model = ShopUser
    form_class = UserCreateForm
    template_name = 'adminapp/form.html'
    success_url = reverse_lazy('adminapp:users')


class CategoryCreate(CallableMixin, AccessMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'adminapp/form.html'
    success_url = reverse_lazy('adminapp:categories')


class ProductCreate(CallableMixin, AccessMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'adminapp/form.html'

    def get_success_url(self):
        return reverse('adminapp:products', kwargs={
            'pk': self.kwargs.get('pk'),
        })

    def get_context_data(self, **kwargs):
        """Добавляем в контекст необходимый объект категории."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            pk=self.kwargs.get('pk'),
        )
        return context

    def form_valid(self, form):
        """Связываем объект категории и созданный объект."""
        context = self.get_context_data()
        category = context.get('category')
        self.object = form.save()
        category.products.add(self.object)
        return HttpResponseRedirect(self.get_success_url())


# алиасы
user_create = UserCreate.as_view()
category_create = CategoryCreate.as_view()
product_create = ProductCreate.as_view()
