from typing import Type

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

from utils.breadcrumbs.mixins import PageTitleMixin
from utils.breadcrumbs.types import Breadcrumb


def reverse_bc(view: Type[PageTitleMixin], url: str = None) -> Breadcrumb:
    """
        Constructs Breadcrumb object using information from view,
        which must be subclass of PageTitleMixin and implement page_title and viewname attributes

    :param view: must be a subclass of PageTitleMixin
    :param url: optional. If specified, used instead of view.viewname
    :return: Breadcrumb
    """
    if not hasattr(view, 'page_title') or (not hasattr(view, 'viewname') or url):
        raise ImproperlyConfigured('view argument must be a subclass of PageTitleMixin')

    if view.page_title and (url or view.viewname):
        return Breadcrumb(view.page_title, reverse_lazy(view.viewname) if not url else url)
    else:
        raise ImproperlyConfigured('view argument must implement both page_title and viewname or implement page_title and pass url')
