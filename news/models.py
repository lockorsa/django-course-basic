from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


class Article(models.Model):
    max_name_length = 64

    name = models.CharField(
        max_length=max_name_length,
        verbose_name='Название',
    )
    body = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Статья опубликована',
    )
    slug = AutoSlugField(
        populate_from='name',
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Метод для получения абсолютного пути в шаблонах."""
        return reverse(viewname='news:article', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created_at',)
