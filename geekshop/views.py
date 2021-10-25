from django.shortcuts import render

from geekshop.models import Product, ProductCategory


def index(request):
    context = {
        'products': Product.objects.all()[:4]
    }
    return render(request, 'geekshop/index.html', context=context)


def contact(request):
    return render(request, 'geekshop/contact.html')


def products(request):
    context = {
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'geekshop/products.html', context=context)


def product_category(request, slug: str):
    context = {
        'category': ProductCategory.objects.get(slug=slug),
    }
    return render(request, 'geekshop/products.html', context=context)
