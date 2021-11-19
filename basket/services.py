from django.core.exceptions import ObjectDoesNotExist

from basket.models import Basket


def get_basket_or_create(user):
    """
    Возвращает или создает для пользователя корзину если ее нет.

    Args:
        user: WSGIRequest.user

    Returns:
        Basket: [Basket instance where owner is user]
        None: [if user not authentificated]
    """
    try:
        return Basket.objects.get(user=user)
    except ObjectDoesNotExist:
        return Basket.objects.create(user=user)
    except TypeError:
        return None
