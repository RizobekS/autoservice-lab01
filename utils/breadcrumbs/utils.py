from typing import Type

from django.urls import reverse_lazy

from apps.site_settings.models import CEOSetting
from utils.breadcrumbs.types import Breadcrumb
from utils.mixins import PageSettingsMixin


def reverse_bc(view: Type[PageSettingsMixin] = None, viewname: str = None, **kwargs) -> Breadcrumb:
    """
        Constructs Breadcrumb object using information from view,
        which must be subclass of PageSettingsMixin and implement page_title and viewname attributes

    :param view: Used to obtain viewname
    :param viewname: Used to find corresponding CEOSetting to construct breadcrumb
    :param kwargs: additional keyword arguments for constructing reverse url
    :return: Breadcrumb
    """
    if hasattr(view, 'viewname'):
        viewname = view.viewname
    elif viewname:
        pass
    else:
        print('''ImproperlyConfigured('Either viewname or view must be correctly set')''')
        # raise ImproperlyConfigured('Either viewname or view must be correctly set')

    ceo_obj = CEOSetting.objects.filter(key=viewname).first()
    if ceo_obj is None:
        print('''ImproperlyConfigured(f'CEOSetting with key="{viewname}" does not exist')''')
        # raise ImproperlyConfigured(f'CEOSetting with key="{viewname}" does not exist')
    else:
        return Breadcrumb(ceo_obj.title, reverse_lazy(ceo_obj.key, kwargs=kwargs))
