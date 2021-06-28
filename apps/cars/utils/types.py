from apps.cars.models import Vendor, Year, Modification, Model, CarFilter
from apps.cars.utils.mixins import CarFilterUtilsMixin
from utils.helpers import exists_or_404


class CarUrls:
    """
    Used for convenient storage for car filter urls
    """
    __slots__ = ('vendor', 'model', 'year', 'modification')

    def __init__(self, vendor=None, model=None, year=None, modification=None):
        self.vendor, self.model, self.year, self.modification = vendor, model, int(year) if year is not None else None, int(modification) if modification is not None else None

    def __repr__(self):
        return f'{self.vendor} {self.model} {self.year} {self.modification}'

    def exists(self) -> bool:
        value = Vendor.objects.filter(url__exact=self.vendor).exists()
        if self.model:
            value = value and Model.objects.filter(url__exact=self.model).exists()
            if self.year:
                value = value and Year.objects.filter(year=self.year).exists()
                if self.modification:
                    value = value and Modification.objects.filter(id=self.modification).exists()
        return value

    def save(self) -> CarFilter:
        """
            Save to database as CarFilter
        """

        kwargs = {}

        obj = Vendor.objects.filter(url__exact=self.vendor)
        kwargs['vendor'] = exists_or_404(obj)

        # Get Model object
        if self.model:
            obj = Model.objects.filter(url__exact=self.model, vendor=kwargs['vendor'])
            kwargs['model'] = exists_or_404(obj)

            # Get Year object
            if self.year:
                obj = Year.objects.filter(year=self.year, model=kwargs['model'])
                kwargs['year'] = exists_or_404(obj)

                # Get Modification object
                if self.modification:
                    obj = Modification.objects.filter(id=self.modification, year=kwargs['year'])
                    kwargs['modification'] = exists_or_404(obj)

        return CarFilter.objects.create(**kwargs)


# class Car(CarFilterUtilsMixin):
#     """
#     The same as CarFilter from .models, but supports partial filling and does not stored in database.
#     """
#     __slots__ = ('vendor', 'model', 'year', 'modification')
#
#     def __init__(self, vendor=None, model=None, year=None, modification=None, urls: CarUrls = None):
#         if urls:
#             self.vendor, self.model, self.year, self.modification = None, None, None, None
#
#             obj = Vendor.objects.filter(url__exact=urls.vendor)
#             self.vendor = exists_or_404(obj)
#
#             # Get Model object
#             if urls.model:
#                 obj = Model.objects.filter(url__exact=urls.model, vendor=self.vendor)
#                 self.model = exists_or_404(obj)
#
#                 # Get Year object
#                 if urls.year:
#                     obj = Year.objects.filter(year=urls.year, model=self.model)
#                     self.year = exists_or_404(obj)
#
#                     # Get Modification object
#                     if urls.modification:
#                         obj = Modification.objects.filter(id=urls.modification, year=self.year)
#                         self.modification = exists_or_404(obj)
#         else:
#             self.vendor, self.model, self.year, self.modification = vendor, model, year, modification
