from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from basket.services import get_basket_or_create
from basket.models import BasketItem
from geekshop.models import Product


@login_required
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


@login_required
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
        basket.products.add(product, through_defaults={'count': 1})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
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
