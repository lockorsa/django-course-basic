from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from adminapp.views.mixins import CallableMixin
from basket.models import BasketItem
from basket.services import get_basket_or_create
from geekshop.models import Product


class LoginRequireMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BasketMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['basket'] = get_basket_or_create(user=self.request.user)
        return context


class BasketList(CallableMixin, LoginRequireMixin, BasketMixin, ListView):
    model = BasketItem
    ordering = ('-count',)
    template_name = 'basket/basket.html'

    def get_queryset(self, *args, **kwargs):
        """Фильтр товаров корзины по принадлежности к пользователю."""
        self.object_list = super().get_queryset(*args, **kwargs)
        # тут будет ошибка если вызвать гет-контекст до гет-кверисет
        basket = self.get_context_data().get('basket')
        return self.object_list.filter(basket=basket)


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


# алиасы
basket = BasketList.as_view()
