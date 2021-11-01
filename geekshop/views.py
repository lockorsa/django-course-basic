from random import choice as random_choice

from django.shortcuts import render

from geekshop.models import Product, ProductCategory


def index(request):
    context = {
        'products': Product.objects.all()[:4]
    }
    return render(request, 'geekshop/index.html', context=context)


def contact(request):
    print(request)
    return render(request, 'geekshop/contact.html')


def products(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'promotion_product': random_choice(Product.objects.all()),
    }
    return render(request, 'geekshop/products.html', context=context)


def product_category(request, slug: str):
    context = {
        'categories': ProductCategory.objects.all(),
        'current_category': ProductCategory.objects.get(slug=slug),
    }
    return render(request, 'geekshop/product_category.html', context=context)
