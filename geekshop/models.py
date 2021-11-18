"""Модели товара и категории/коллекции товаров."""
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    """Абстрактный класс, наследуемый товарами и категориями."""

    max_length = 32

    name = models.CharField(
        max_length=max_length,
        verbose_name='Название',
        unique=True,
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения',
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True,
        unique_with='name',
        verbose_name='URL',
    )
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_active = not self.is_active
        self.save()

    def __str__(self):
        """Возвращает название продукта/категории."""
        return self.name

    class Meta(object):
        """Делает класс доступным для наследования."""

        abstract = True


class Category(BaseModel):
    """
    Категория/коллекция товаров.

    Категория имеет свой url и может ссылаться на любое количество товаров.
    """

    products = models.ManyToManyField(
        'Product',
        related_name='categories',
        verbose_name='Товары в категории',
    )

    def get_absolute_url(self):
        """Метод для получения абсолютного пути в шаблонах."""
        return reverse(
            viewname='geekshop:category',
            kwargs={'slug': self.slug},
        )

    class Meta(object):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(BaseModel):
    """
    Товар магазина.

    Товар добавляет к стандартным полям цену, количество и фото.
    """

    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name='Цена',
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество в наличии',
    )
    image = models.ImageField(
        upload_to='products',
        verbose_name='Фото',
    )

    def get_absolute_url(self):
        """Метод для получения абсолютного пути в шаблонах."""
        return reverse(
            viewname='geekshop:product',
            kwargs={'slug': self.slug},
        )

    class Meta(object):
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
