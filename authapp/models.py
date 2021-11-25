import datetime
import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    max_key_length = 128
    nullable = {'blank': True, 'null': True}

    avatar = models.ImageField(
        upload_to='user_avatars',
        blank=True,
        verbose_name='Аватар',
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения',
    )
    register_activation_key = models.CharField(
        max_length=max_key_length,
        verbose_name='Ключ активации',
        **nullable,
    )
    activation_key_expired = models.DateTimeField(
        verbose_name='Срок действия ключа активации',
        **nullable,
    )

    def activate(self):
        self.is_active = True
        self.register_activation_key = None
        self.activation_key_expired = None
        self.save()

    def is_activation_key_expired(self) -> bool:
        """
        Проверка срока годности ключа активации.

        Нужно дописать проверку если ключ = NULL
        """
        return datetime.datetime.now(
            pytz.timezone(settings.TIME_ZONE),
            ) > self.activation_key_expired

    @property
    def age(self) -> int:
        """
        Вычисляет возраст пользователя.

        Требует рефакторинга
        """
        today = datetime.date.today()
        return today.year - self.birth_date.year - (
            (
                today.month,
                today.day,
            ) < (
                self.birth_date.month,
                self.birth_date.day,
            ))

    def delete(self):
        self.is_active = not self.is_active
        self.save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
