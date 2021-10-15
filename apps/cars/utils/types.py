from apps.cars.models import Vendor, Year, Modification, Model, CarFilter
from utils.shortcuts import exists_or_404


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
        value = Vendor.objects.filter(url__exact=self.vendor, active=True).exists()
        if self.model:
            value = value and Model.objects.filter(url__exact=self.model, active=True).exists()
            if self.year:
                value = value and Year.objects.filter(year=self.year, model__url__exact=self.model).exists()
                if self.modification:
                    value = value and Modification.objects.filter(id=self.modification).exists()
        return value

    def save(self, request) -> CarFilter:
        """
            Save to database as CarFilter
        """
        car_filter = None
        kwargs = {'model': None, 'year': None, 'modification': None}

        obj = Vendor.objects.filter(url__exact=self.vendor, active=True)
        kwargs['vendor'] = exists_or_404(obj)

        # Get Model object
        if self.model:
            obj = Model.objects.filter(url__exact=self.model, vendor=kwargs['vendor'], active=True)
            kwargs['model'] = exists_or_404(obj)

            # Get Year object
            if self.year:
                obj = Year.objects.filter(year=self.year, model=kwargs['model'])
                kwargs['year'] = exists_or_404(obj)

                # Get Modification object
                if self.modification:
                    obj = Modification.objects.filter(id=self.modification, year=kwargs['year'])
                    kwargs['modification'] = exists_or_404(obj)
                    if request.user.is_authenticated:
                        kwargs['user'] = request.user
                        car_filter, created = CarFilter.objects.get_or_create(**kwargs)
                        if not created:
                            car_filter.update_last_used()
        if car_filter is None:
            car_filter = CarFilter.objects.create(**kwargs)
        return car_filter
