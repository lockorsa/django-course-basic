from django.db import models


class Basket(models.Model):
    user = models.OneToOneField(
        'authapp.ShopUser',       # заменить на юзера из settings(django.conf)
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
    )
    products = models.ManyToManyField(
        'geekshop.Product',
        through='BasketItem',
        through_fields=('basket', 'product'),
        verbose_name='Товары',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def drop_all_products(self):
        """Удаляет все продукты из корзины"""
        pass

    @property
    def products_count(self) -> int:
        total_count = 0
        basket_items = BasketItem.objects.filter(basket=self)
        for basket_item in basket_items:
            total_count += basket_item.count
        return total_count

    @property
    def products_price(self) -> int:
        total_price = 0
        basket_items = BasketItem.objects.filter(basket=self)
        for basket_item in basket_items:
            total_price += basket_item.count * basket_item.product.price
        return total_price

    class Meta:
        verbose_name = 'Корзина покупателя'
        verbose_name_plural = 'Корзины покупателей'


class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'geekshop.Product',
        on_delete=models.CASCADE,
    )
    count = models.PositiveSmallIntegerField(default=0)
