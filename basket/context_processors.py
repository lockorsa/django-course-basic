from basket.services import get_basket_or_create


def basket(request):
    basket_obj = get_basket_or_create(request.user)
    return {'basket': basket_obj}
