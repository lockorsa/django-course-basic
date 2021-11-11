"""Модели товара и категории/коллекции товаров."""
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    """
    Абстрактный класс, наследуемый товарами и категориями.

    объединяет стандартные поля:
    [name, description, created_at, updated_at]
    """

    max_length = 32

    name = models.CharField(
        max_length=max_length,
        verbose_name='Название',
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

    Наследует поля:
    [name, description, created_at, updated_at]

    Наследует методы:
    [__str__]
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
    Товар в магазине.

    Товар имеет свою цену, количество и фото.

    Наследует поля:
    [name, description, created_at, updated_at, slug(url)]

    Наследует методы:
    [__str__]
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
