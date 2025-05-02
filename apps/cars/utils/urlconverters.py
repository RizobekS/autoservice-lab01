from apps.cars.utils.types import CarUrls


class CarPathConverter:
    regex = r'[a-z0-9\-]+(?:/[a-z0-9\-]+){0,3}'

    def to_python(self, value: str) -> CarUrls:
        values = value.split('/')
        values = values[:4]
        car_urls = CarUrls(*values)
        if not car_urls.exists():
            raise ValueError(f'Car with url {value} does not exist')
        return car_urls

    def to_url(self, components) -> str:
        return '/'.join(components) if isinstance(components, (tuple, list)) else components


class OldCarPathConverter:
    regex = r'[a-z0-9\-]+(?:--[a-z0-9\-]+){1,3}'

    def to_python(self, value: str) -> CarUrls:
        values = value.split('--')
        car_urls = CarUrls(*values)
        if not car_urls.exists() or not car_urls.vendor or not car_urls.model:
            raise ValueError(f'Некорректные данные car_urls: {value}')
        return car_urls

    def to_url(self, components) -> str:
        return '--'.join(components) if isinstance(components, (tuple, list)) else components
