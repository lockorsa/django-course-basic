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


class ProductList(BasketMixin, CategoryMixin, ListView):
    """Один контроллер, чтобы править всеми."""

    model = Product
    ordering = ('-price',)
    template_name = 'geekshop/products.html'

    def get_queryset(self):
        """
        Наличие слага категории определяет возвращаемый объект.

        Returns:
            [Product_queryset]: список товаров категории
            [promotion_product]: рекламный продукт, если запрос без слага
        """
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug', False)
        if slug:
            self.context_object_name = 'products'
            self.object_list = queryset.filter(categories__slug=slug)
            # добавляем в контекст запрашиваемую категорию
            self.extra_context = {
                'current_category': Category.objects.get(slug=slug),
            }
        else:
            self.context_object_name = 'promotion_product'
            self.object_list = get_promotion_product()
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
products = ProductList.as_view()
product_detail = ProductDetail.as_view()
