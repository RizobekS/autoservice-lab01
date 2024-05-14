import json
import os
from collections import defaultdict
from timeit import default_timer
from typing import Tuple

import MySQLdb
from django.conf import settings
from django.db import transaction

from apps.cars.models import Vendor, Model, Year, Modification

CREATED = defaultdict(int)
OVERALL = defaultdict(int)


def fetch_data():
    # Create connection
    db = MySQLdb.connect(host=settings.DATABASES['default']['HOST'], user=settings.DATABASES['default']['USER'], password=settings.DATABASES['default']['PASSWORD'],
                         database="autoservice_new_cars")

    # Create cursor
    cursor = db.cursor()

    # Execute SQL query
    cursor.execute("SELECT vendor, car, year, modification FROM search_by_vehicle")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close connection
    db.close()

    # Return rows data
    return rows


def create_row_if_needed(row: Tuple[str, str, str, str]):
    raw_vendor, raw_car, raw_year, raw_modification = map(str.strip, row)

    vendor = Vendor.objects.filter(name=raw_vendor).first()
    if vendor is None:
        vendor = Vendor.objects.create(name=raw_vendor)
        CREATED['vendor'] += 1
    OVERALL['vendor'] += 1

    model = Model.objects.filter(name=raw_car, vendor_id=vendor.pk).first()
    if model is None:
        model = Model.objects.create(name=raw_car, vendor=vendor)
        CREATED['model'] += 1
    OVERALL['model'] += 1

    year = Year.objects.filter(year=raw_year, model_id=model.pk).first()
    if year is None:
        year = Year.objects.create(year=raw_year, model=model)
        CREATED['year'] += 1
    OVERALL['year'] += 1

    modification = Modification.objects.filter(name=raw_modification, year_id=year.pk).first()
    if modification is None:
        modification = Modification.objects.create(name=raw_modification, year=year)
        CREATED['modification'] += 1
    OVERALL['modification'] += 1


def remove_existing_objects_from_fixture():
    existing_path = os.path.join(settings.PROJECT_ROOT, 'dumps', 'cars.json')
    all_path = os.path.join(settings.PROJECT_ROOT, 'dumps', 'all_cars.json')
    new_path = os.path.join(settings.PROJECT_ROOT, 'dumps', 'new_cars.json')

    existing = defaultdict(set)
    new = defaultdict(list)

    with open(existing_path, encoding='utf-8') as file:
        data = json.load(file)

        for obj in data:
            existing[obj['model']].add(obj['pk'])

    print(f'Existing vendors: {len(existing["cars.vendor"])}\n'
          f'\tmodels: {len(existing["cars.model"])}'
          f'\tyears: {len(existing["cars.year"])}'
          f'\tmodifications: {len(existing["cars.modification"])}')

    with open(all_path, encoding='utf-8') as file:
        data = json.load(file)

        for obj in data:
            if obj['pk'] not in existing[obj['model']]:
                new[obj['model']].append(obj)

    print(f'New vendors: {len(new["cars.vendor"])}\n'
          f'\tmodels: {len(new["cars.model"])}'
          f'\tyears: {len(new["cars.year"])}'
          f'\tmodifications: {len(new["cars.modification"])}')

    with open(new_path, 'w', encoding='utf-8') as file:
        data = [
            *new["cars.vendor"],
            *new["cars.model"],
            *new["cars.year"],
            *new["cars.modification"],
        ]
        json.dump(data, file)


def main():
    start = default_timer()
    data = fetch_data()
    print(f'Fetch {len(data)} rows in {default_timer() - start:.2f} seconds')

    with transaction.atomic():
        for row in data:
            create_row_if_needed(row)

    print(f'Vendors: {CREATED["vendor"]}/{OVERALL["vendor"]}\n'
          f'model: {CREATED["model"]}/{OVERALL["model"]}\n'
          f'year: {CREATED["year"]}/{OVERALL["year"]}\n'
          f'modification: {CREATED["modification"]}/{OVERALL["modification"]}\n')
