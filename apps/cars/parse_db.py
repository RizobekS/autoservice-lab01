#!/usr/bin/python3

def start():
    import pymysql

    # Open database connection
    from apps.cars.models import Vendor, Model, Year, Modification

    db = pymysql.connect(host="localhost", user="dabud", password="8ghgVa7k_5Y7LK*", db="autoservice", charset="utf8mb4")
    print('Connected to the database')

    cursor = db.cursor()
    cursor.execute("SELECT search_by_vehicle.vendor, search_by_vehicle.car, search_by_vehicle.year, search_by_vehicle.modification FROM search_by_vehicle")
    print('Executed SELECT')
    row = cursor.fetchone()
    print('Started parsing rows')

    while row is not None:
        # Find or create vendor
        name = row[0].strip()
        vendor = Vendor.objects.get(name=name) if Vendor.objects.filter(name=name).exists() else Vendor.objects.create(name=name)

        # Find or create model
        name = row[1].strip()
        model = Model.objects.get(name=name, vendor=vendor) if Model.objects.filter(name=name, vendor=vendor).exists() else Model.objects.create(name=name, vendor=vendor)

        # Find or create year
        value = row[2].strip()
        year = Year.objects.get(year=value, model=model) if Year.objects.filter(year=value, model=model).exists() else Year.objects.create(year=value, model=model)

        # Find or create modification
        name = row[3].strip()
        modification = Modification.objects.get(name=name, year=year) if Modification.objects.filter(name=name, year=year).exists() else Modification.objects.create(name=name,
                                                                                                                                                                     year=year)

        row = cursor.fetchone()
        print(f'Added "{modification}", fetching next one')

    db.close()
    print('Finished, disconnecting from the database')
