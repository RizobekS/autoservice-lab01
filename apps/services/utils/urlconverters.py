from apps.services.models import Section


class SectionUrlFilter:
    regex = '.+'

    def to_python(self, value: str) -> str:
        exists = Section.objects.filter(url__exact=value).exists()
        if not exists:
            raise ValueError(f'Section with url={value} does not exist')
        return value

    def to_url(self, value) -> str:
        return value
