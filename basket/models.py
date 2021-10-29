from django.db import models


class OrderItem(models.Model):
    user = models.ForeignKey('authapp.ShopUser', on_delete=models.CASCADE)
    product = models.ForeignKey('geekshop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
