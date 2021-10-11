#!/usr/bin/python3
from timeit import default_timer

import pymysql

from apps.cars.models import Vendor, Model, Year, Modification


def start():
    VENDOR_SET = ('Skoda', 'Audi', 'Nissan', 'BMW', 'Renault', 'Opel', 'Volkswagen', 'Hyundai', 'Kia', 'Toyota', 'Chery', 'Mitsubishi')

    db = pymysql.connect(host="localhost", user="dabud", password="8ghgVa7k_5Y7LK*", db="autoservice", charset="utf8mb4")
    print('Connected to the database')

    cursor = db.cursor()
    cursor.execute(f"""SELECT COUNT(*) FROM search_by_vehicle""")
    overall = cursor.fetchone()[0]
    print(f'Overall entries found: {overall}')

    cursor.execute(f"""SELECT search_by_vehicle.vendor, search_by_vehicle.car, search_by_vehicle.year, search_by_vehicle.modification FROM search_by_vehicle""")
    print('Executed SELECT')
    rows = cursor.fetchall()
    print('Started parsing rows')

    counter = 0
    time_counter = 1
    overall_time = 0
    for row in rows:
        time_start = default_timer()
        # Find or create vendor
        name = row[0].strip()
        vendor, vendor_created = Vendor.objects.get_or_create(name=name)

        # Find or create model
        name = row[1].strip()
        model, model_created = Model.objects.get_or_create(name=name, vendor=vendor)

        # Find or create year
        value = row[2].strip()
        year, year_created = Year.objects.get_or_create(year=value, model=model)

        # Find or create modification
        name = row[3].strip()
        modification, modification_created = Modification.objects.get_or_create(name=name, year=year)

        # Determines whether this iteration can contribute into time estimating
        time_counts = vendor_created or model_created or year_created or modification_created

        counter += 1
        time_counter += int(time_counts)
        print(f'\nAdded "{modification}"')
        overall_time += default_timer() - time_start if time_counts else 0
        time_remaining = (overall_time / time_counter) * (overall - counter)
        print(f'{counter: 5}/{overall}. Time db time elapsed: {int(overall_time // 60)}:{int(overall_time % 60):02}'
              f'\nEstimated time until finish:     {int(time_remaining // 60)}:{int(time_remaining % 60):02}')

    db.close()
    print('Finished, disconnecting from the database')
