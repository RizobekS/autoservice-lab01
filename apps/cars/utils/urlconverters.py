from apps.cars.utils.types import CarUrls


class CarPathConverter:
    regex = '.+'  # (?!.*--)

    def to_python(self, value: str) -> CarUrls:
        values = value.split('--')
        car_urls = CarUrls(*values)
        if not car_urls.exists():
            raise ValueError(f'Car with url {value} does not exist')
        return car_urls

    def to_url(self, components) -> str:
        return '--'.join(components) if isinstance(components, (tuple, list)) else components
