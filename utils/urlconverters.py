class BaseModelUrlFilter:
    regex = r'[a-z0-9\-]+'

    @property
    def model_class(self):
        raise NotImplementedError()

    @property
    def url_field_name(self):
        raise NotImplementedError()

    def to_python(self, value: str) -> str:
        kwargs = {f'{self.url_field_name}__exact': value}

        exists = self.model_class.objects.filter(**kwargs).exists()
        if not exists:
            raise ValueError(f'{self.model_class.__name__} with url={value} does not exist')
        return value

    def to_url(self, value) -> str:
        return value


def url_converter_factory(model_class: type, url_field_name: str = 'url') -> object:
    """ Returns url converter that checks whether a requested url is present in database in a given model """
    return type(
        f'{model_class.__name__}UrlConverter',
        (BaseModelUrlFilter,),
        {'model_class': model_class,
         'url_field_name': url_field_name}
    )
