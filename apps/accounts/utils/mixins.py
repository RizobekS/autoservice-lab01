from enum import Enum
from typing import Dict, Any

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin

from utils.breadcrumbs.mixins import BreadcrumbsMixin
from utils.breadcrumbs.types import Breadcrumb


class MenuItem(Enum):
    INDEX = 1
    ORDERS = 2
    GARAGE = 3
    PERSONAL_DATA = 4

    def is_index(self) -> bool:
        return self == MenuItem.INDEX

    def is_orders(self) -> bool:
        return self == MenuItem.ORDERS

    def is_garage(self) -> bool:
        return self == MenuItem.GARAGE

    def is_personal_data(self) -> bool:
        return self == MenuItem.PERSONAL_DATA


class MenuMixin(ContextMixin):
    """
        Automatically updates your context

        menu: MenuItem - represents current menu level
    """

    menu = None

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu_item'] = self.menu
        return context


class PersonalAreaMixin(BreadcrumbsMixin, MenuMixin):
    """
        Adds necessary context for Personal area, helps building breadcrumbs and aside menu

    """
    initial_breadcrumbs = [Breadcrumb('Личный кабинет', reverse_lazy('accounts:pa:index'))]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        extra_context = {
            'page_title': 'Личный кабинет',
            'image_url': static('images/lk/lk-header.jpg'),
            'image_alt': 'Retro car',
        }
        context.update(extra_context)
        return context
