from random import choice as random_choice

from django.shortcuts import get_object_or_404, render

from basket.services import get_basket_or_create
from geekshop.models import Product, ProductCategory


def products(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'promotion_product': random_choice(Product.objects.all()),
        'basket': get_basket_or_create(request.user),
    }
    return render(request, 'geekshop/products.html', context=context)


def product_category(request, slug: str):
    context = {
        'categories': ProductCategory.objects.all(),
        'current_category': get_object_or_404(ProductCategory, slug=slug),
        'basket': get_basket_or_create(request.user),
    }
    return render(request, 'geekshop/product_category.html', context=context)


def product(request, slug: str):
    context = {
        'categories': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, slug=slug),
        'basket': get_basket_or_create(request.user),
    }
    return render(request, 'geekshop/product.html', context=context)
