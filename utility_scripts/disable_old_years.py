from django.db import transaction
from django.db.models import Q, Count

from apps.cars.models import Year, Model


def main():
    with transaction.atomic():
        years = Year.objects.filter(year__lt=2005, active=True)

        years.update(active=False)

        print(f'Disabled {years.count()} Year instances')

        mods = 0
        for year in years:
            qs = year.active_modification_set()

            qs.update(active=False)

            mods += qs.count()

        print(f'Disabled {mods} modifications')

        qs = Model.objects.annotate(
            count=Count('year', filter=Q(year__active=True))
        ).filter(count=0)

        qs.update(active=False)

        print(f'Disabled {qs.count()} models')
