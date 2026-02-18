from django.db import connection
from apps.services.models import CarPack


class CachedCarsAll:
    """
        Optimizes creating car urls by caching list of computed car's url parts (for products with all cars)
    """
    __slots__ = ('_items',)

    def __call__(self, *args, **kwargs):
        if not getattr(self, '_items', None):
            self._items = self.all_cars()
        return self._items

    @staticmethod
    def all_cars():
        """
            This function performs raw database query (for the sake of performance) to find all cars
            and extract all url components for distinct vendor, distinct vendor+model, distinct vendor+model+year+modification.
        """
        urls = set()

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT cars_vendor.url, cars_model.url, cars_year.year, cars_modification.id
                    FROM cars_vendor JOIN cars_model ON cars_vendor.id=cars_model.vendor_id
                                     JOIN cars_year ON cars_model.id = cars_year.model_id
                                     JOIN cars_modification ON cars_year.id = cars_modification.year_id
                    WHERE cars_vendor.active = 1 AND cars_model.active = 1"""
            )
            for item in cursor.fetchall():
                urls.add((item[0],))  # vendor
                urls.add((item[0], item[1]))  # vendor + model
        return list(urls)


class CachedCarsCarPack:
    """
        Optimizes creating car urls by caching list of computed car's url parts (for some car pack)
    """
    __slots__ = ('_items', 'car_pack')

    def __init__(self, car_pack):
        if type(car_pack) is not CarPack:
            raise ValueError(f'CachedCarsCarPack: car_pack must be instance of CarPack, not {type(car_pack)}')
        self.car_pack = car_pack

    def __call__(self, *args, **kwargs):
        if not getattr(self, '_items', None):
            self._items = self.for_car_pack()
        return self._items

    def for_car_pack(self):
        """
            This function performs raw database query (for the sake of performance) to find all cars (with active vendor and model), corresponding to
            specified car_pack and extract all url components for distinct vendor, distinct vendor+model, distinct vendor+model+year+modification.
        """
        urls = set()

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT cars_vendor.url, cars_model.url, cars_year.year, cars_modification.id
                    FROM cars_vendor JOIN cars_model ON cars_vendor.id=cars_model.vendor_id
                                     JOIN cars_year ON cars_model.id = cars_year.model_id
                                     JOIN cars_modification ON cars_year.id = cars_modification.year_id
                    WHERE cars_vendor.active = 1 AND cars_model.active = 1 AND cars_modification.id IN (SELECT modification_id
                                                                                                        FROM services_carpack_cars
                                                                                                        WHERE carpack_id = %s)""",
                [self.car_pack.id]
            )
            for item in cursor.fetchall():
                urls.add((item[0],))  # vendor
                urls.add((item[0], item[1]))  # vendor + model
        return list(urls)


def create_cached_car_url_list(car_pack):
    """
        This returns an executable class, which computes url components for given car_pack (for all car_packs if None)
        when this class is called (and caches the result)
    """
    if car_pack is None:
        return CachedCarsAll()
    else:
        return CachedCarsCarPack(car_pack)
