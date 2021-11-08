from django.shortcuts import get_object_or_404, render

from basket.services import get_basket_or_create
from geekshop.models import Product


def index(request):
    context = {
        'products': Product.objects.all()[:4],
        'basket': get_basket_or_create(request.user),
    }
    return render(request, 'index/index.html', context=context)


def contact(request):
    context = {
        'basket': get_basket_or_create(request.user),
    }
    return render(request, 'index/contact.html', context=context)
