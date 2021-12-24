from django.views.generic.base import ContextMixin

from apps.site_settings.models import StaticInformation


class OpengraphMixin(ContextMixin):
    """
        This mixin automates specifying OpenGraph tags.
        If this mixin is added to the view - all metatags are automatically inserted into HTML response.
    """

    og_type = 'website'
    og_locale = 'ru_RU'

    def __init__(self):
        site_name = StaticInformation.objects.get(key='site_name')
        self.og_site_name = site_name.value

    def get_og_tags(self, **kwargs) -> dict:
        return {'type': self.og_type,
                'locale': self.og_locale,
                'site_name': self.og_site_name,
                **kwargs}

    def _processed_og_tags(self):
        def check_prefix(string: str):
            return string if string.startswith('og:') else f'og:{string}'

        return {check_prefix(key): value for key, value in self.get_og_tags().items()}

    def get_context_data(self, **kwargs):
        kwargs['opengraph_metatags'] = self._processed_og_tags()
        return super().get_context_data(**kwargs)
