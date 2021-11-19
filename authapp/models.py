import datetime as dt 
from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='user_avatars',
        blank=True,
        verbose_name='Аватар',
    )
    birth_date = models.DateField(verbose_name='Дата рождения')

    def delete(self):
        self.is_active = not self.is_active
        self.save()

    @property
    def age(self):
        """
        Вычисляет сколько лет пользователю.

        Требует рефакторинга
        """
        today = dt.date.today()
        return today.year - self.birth_date.year - \
            ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
