from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from basket.models import Basket, BasketItem
from geekshop.models import Product


def basket(request):
    basket = get_basket_or_create(user=request.user)
    basket_items = BasketItem.objects.filter(
        basket=basket,
    )
    context = {
        'basket': basket,
        'basket_items': basket_items,
    }
    return render(request, 'basket/basket.html', context=context)


def add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = get_basket_or_create(user=request.user)

    if product in basket.products.all():
        basket_item = BasketItem.objects.get(
            basket=basket,
            product=product,
        )
        basket_item.count += 1
        basket_item.save()
    else:
        basket.products.add(product, through_defaults={
            'count': 1,
        })

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = get_basket_or_create(user=request.user)

    basket_item = BasketItem.objects.get(
        basket=basket,
        product=product,
    )
    basket_item.count -= 1
    basket_item.save()
    
    if basket_item.count == 0:
        basket.products.remove(product)
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_basket_or_create(user):
    try:
        user_basket = Basket.objects.get(user=user)
    except ValueError:
        user_basket = Basket.objects.create(user=user)
    return user_basket
