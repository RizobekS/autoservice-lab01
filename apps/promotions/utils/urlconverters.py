from apps.promotions.models import Category


class CategoryUrlFilter:
    regex = '.+'

    def to_python(self, value: str) -> str:
        exists = Category.objects.filter(url__exact=value).exists()
        if not exists:
            raise ValueError(f'Promotion Category with url={value} does not exist')
        return value

    def to_url(self, value) -> str:
        return value
