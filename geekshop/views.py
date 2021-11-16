from django.shortcuts import get_object_or_404, render

from basket.services import get_basket_or_create
from geekshop.services import get_promotion_product
from geekshop.models import Product, Category


def products(request):
    context = {
        'basket': get_basket_or_create(request.user),
        'categories': Category.objects.filter(is_active=True),
        'promotion_product': get_promotion_product(),
    }
    return render(request, 'geekshop/products.html', context=context)


def product_category(request, slug: str):
    context = {
        'basket': get_basket_or_create(request.user),
        'categories': Category.objects.filter(is_active=True),
        'current_category': get_object_or_404(
            Category,
            slug=slug,
            is_active=True,
        ),
    }
    return render(request, 'geekshop/product_category.html', context=context)


def product(request, slug: str):
    context = {
        'basket': get_basket_or_create(request.user),
        'categories': Category.objects.filter(is_active=True),
        'product': get_object_or_404(Product, slug=slug, is_active=True),
    }
    return render(request, 'geekshop/product.html', context=context)
