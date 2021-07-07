from typing import Any, Dict

from django.core.exceptions import ImproperlyConfigured
from django.template import Template, Context
from django.views.generic.base import ContextMixin

from apps.site_settings.models import MetaTag


class MetaTagsRenderer:
    """
        Has methods to render meta tags "description", "keywords" and "robots"
        Subclasses MUST implement meta_tags_key attribute and either meta_context or get_meta_context()
        get_meta_context() must return context dictionary
    """
    meta_tags_key = None
    meta_context = None

    def __init__(self, meta_tags_key=None, meta_context=None):
        self.meta_tags_key = meta_tags_key
        self.meta_context = meta_context

    def _render(self, field_name):
        meta_object = self.get_meta_tags_object()
        attr = getattr(meta_object, field_name)

        if attr and meta_object.variables:
            template = Template(attr)
            return template.render(Context(self.get_meta_context()))
        else:
            return attr

    def get_meta_tags_key(self):
        if self.meta_tags_key is None:
            raise ImproperlyConfigured('You must implement meta_tags_key attribute')
        return self.meta_tags_key

    def get_meta_tags_object(self):
        key = self.get_meta_tags_key()
        meta_tag = MetaTag.objects.filter(key=key)
        if not meta_tag.exists():
            raise ImproperlyConfigured(f'MetaTag with key={key} does not exist')
        return meta_tag.first()

    def get_meta_context(self) -> Dict[str, Any]:
        return self.meta_context

    def description(self):
        return self._render('description')

    def keywords(self):
        return self._render('keywords')

    def robots(self):
        return self._render('robots')

    def as_context(self):
        return {
            'meta_description': self.description(),
            'meta_keywords': self.keywords(),
            'meta_robots': self.robots(),
        }


class MetaTagsMixin(ContextMixin, MetaTagsRenderer):
    """
        Adds meta_description, meta_keywords and meta_robots to your context
        overrides get_meta_tags_key() to fallback to viewname if available
    """

    def get_meta_tags_key(self):
        return self.viewname if hasattr(self, 'viewname') and self.viewname else super().get_meta_tags_key()

    def get_context_data(self, **kwargs):
        kwargs.update(self.as_context())
        return super().get_context_data(**kwargs)
