from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from basket.views import BasketMixin
from geekshop.models import Category, Product
from geekshop.services import get_promotion_product


class CategoryMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class ProductRoot(BasketMixin, CategoryMixin, DetailView):
    context_object_name = 'promotion_product'
    template_name = 'geekshop/products.html'

    def get_object(self):
        return get_promotion_product()


class ProductList(BasketMixin, CategoryMixin, ListView):
    model = Product
    context_object_name = 'products'
    ordering = ('-price',)
    paginate_by = 2
    template_name = 'geekshop/products.html'

    def get_queryset(self):
        """Фильтрация товаров по категории и добавление в контекст."""
        slug = self.kwargs.get('slug')
        # фильтруем товары по категории
        self.object_list = super().get_queryset().filter(
            categories__slug=slug,
        )
        # добавляем в контекст запрашиваемую категорию
        self.extra_context = {
            'current_category': Category.objects.get(slug=slug),
        }
        return self.object_list


class ProductDetail(BasketMixin, CategoryMixin, DetailView):
    model = Product
    template_name = 'geekshop/product_detail.html'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст категорию товара."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            pk=self.object.categories.first().pk,
        )
        return context


# алиасы
root = ProductRoot.as_view()
products = ProductList.as_view()
product_detail = ProductDetail.as_view()
