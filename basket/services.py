from django.core.exceptions import ObjectDoesNotExist

from basket.models import Basket


def get_basket_or_create(user):
    try:
        return Basket.objects.get(user=user)
    except TypeError:
        return None
    except ObjectDoesNotExist:
        return Basket.objects.create(user=user)
