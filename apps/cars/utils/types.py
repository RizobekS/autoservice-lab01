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
            if request.user.is_authenticated:
                kwargs['user'] = request.user
                car_filter, created = CarFilter.objects.get_or_create(**kwargs)
                if not created:
                    car_filter.update_last_used()
        if car_filter is None:
            car_filter = CarFilter.objects.create(**kwargs)
        return car_filter

    def url_args(self):
        """
        Возвращает только валидные URL-части (vendor, model[, year, modification])
        """
        args = [self.vendor, self.model]
        if self.year is not None:
            args.append(str(self.year))
        if self.modification is not None:
            args.append(str(self.modification))
        return args
