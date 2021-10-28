import datetime as dt

from django.core.management.base import BaseCommand

from authapp.models import ShopUser


class Command(BaseCommand):
    age_limit = 18

    def handle(self, *args, **options):
        birth_date = self.get_date_above_age_limit()
        
        ShopUser.objects.create_superuser(
            'django',
            'django@geekshop.local',
            'geekbrains',
            birth_date=birth_date,
        )

    def get_date_above_age_limit(self) -> dt.date:
        return dt.date.today() - dt.timedelta(days=self.age_limit * 366)
